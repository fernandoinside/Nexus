# Usando uma imagem leve de Python
FROM python:3.9-slim

# Diretório de trabalho dentro do contêiner
WORKDIR /app

# Copiar os arquivos do projeto
COPY . /app

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta definida no .env
EXPOSE ${APP_PORT}

# Comando para rodar a aplicação
CMD ["python", "main.py"]
