import boto3
import pandas as pd
import io
import time


import os

BUCKET = os.getenv("S3_BUCKET", "bucket-coretrace")
SILVER = "trusted/"
GOLD = "gold/"

s3 = boto3.client("s3")


def preparar_dados(df):

    df = df.copy()

    identificadores = ["TIMESTAMP", "ENDERECO_MAC"]

    metricas = [
        coluna for coluna in df.columns
        if coluna not in identificadores
    ]

    df_gold = df.melt(
        id_vars=identificadores,
        value_vars=metricas,
        var_name="METRICA",
        value_name="VALOR"
    )

    df_gold["VALOR"] = pd.to_numeric(
        df_gold["VALOR"],
        errors="coerce"
    )

    df_gold = df_gold.dropna(
        subset=["VALOR"]
    )

    return df_gold


def gerar_gold():

    print("Buscando dados na Silver...")

    paginator = s3.get_paginator("list_objects_v2")

    paginas = paginator.paginate(
        Bucket=BUCKET,
        Prefix=SILVER
    )

    tabelas = []

    for pagina in paginas:

        for arquivo in pagina.get("Contents", []):

            chave = arquivo["Key"]

            nome_arquivo = chave.split("/")[-1]

            if not nome_arquivo.startswith("coretrace_coleta_"):
                continue

            if not nome_arquivo.lower().endswith(".csv"):
                continue

            resposta = s3.get_object(
                Bucket=BUCKET,
                Key=chave
            )

            conteudo = resposta["Body"].read()

            df = pd.read_csv(
                io.BytesIO(conteudo)
            )

            if df.empty:
                continue

            df_gold = preparar_dados(df)

            tabelas.append(df_gold)

            print("Arquivo processado:", nome_arquivo)

    if not tabelas:

        print("Nenhum dado encontrado na Silver.")
        return

    gold = pd.concat(
        tabelas,
        ignore_index=True
    )

    gold = gold.drop_duplicates()

    gold = gold.sort_values(
        ["TIMESTAMP", "ENDERECO_MAC", "METRICA"]
    )

    csv_gold = gold.to_csv(
        index=False
    )

    destino = GOLD + "metricas_dashboard.csv"

    s3.put_object(
        Bucket=BUCKET,
        Key=destino,
        Body=csv_gold.encode("utf-8"),
        ContentType="text/csv; charset=utf-8"
    )

    print("Gold enviada para:", destino)


if __name__ == "__main__":

    while True:

        try:

            print("\nIniciando processamento Gold...")

            gerar_gold()

            print("Aguardando 5 minutos...")

        except Exception as erro:

            print("Erro no processamento Gold:", erro)

        time.sleep(300)