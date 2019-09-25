# Imagem base.
FROM python:3.7.4

# Necessário para rodar nc no script de entrypoint.
RUN apt-get update && apt-get install -y netcat

# Configura o diretório base do container.
WORKDIR /app

# Copia o requirements.txt para o container e instala as deps.
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copia o restante do projeto.
COPY . /app

# Habilita o script de entrypoint.
COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Roda o server de desenvolvimento, após a conexão com o banco se realizar.
CMD ["/app/entrypoint.sh"]