
FROM python:3.12-slim


WORKDIR /app


RUN pip install --no-cache-dir boto3 pandas numpy


COPY transformer.py load.py ./

ENV PYTHONUNBUFFERED=1

CMD ["sh", "-c", "python transformer.py & python load.py & wait"]



# passos de como fzr para rodar com .env de parametro e testar os logs

#primeiro = rodar a imagem: docker build -t coretrace-etl


  #docker run -d --name coretrace-teste `
  #--env-file .env `
  #-v "${env:USERPROFILE}\.aws:/root/.aws:ro" `
  #coretrace-etl 

  #pra testar rode : 
    #docker exec coretrace-teste(nome do container) printenv S3_BUCKET
    #docker exec coretrace-teste(nome do container) printenv AWS_DEFAULT_REGION

    #pra fzr os testes dos logs
    #docker logs --tail 40 coretrace-teste(core-trace-teste é o nome do container)
    #vai ser testado com base no s3 bucket-coretrace

