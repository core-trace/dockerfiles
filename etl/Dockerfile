#usa imagem pronta
FROM python:3.12-slim

#a pasta /app vira diretorio
WORKDIR /app

#instala as bibliotecas usadas

RUN pip install --no-cache-dir boto3 pandas numpy

# Copia os dois arquivos Python do computador para a imagem docker
COPY transformer.py load.py ./

ENV PYTHONUNBUFFERED=1
# inicia a ETL de transformação e depois a de carregar
CMD ["sh", "-c", "python transformer.py & python load.py & wait"]

#rodar a imagem: docker build -t coretrace-etl .