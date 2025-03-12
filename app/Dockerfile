# Usando uma imagem leve de Python
FROM python:3.9-slim

# Instalar dependências do sistema necessárias para o TTS
RUN apt-get update && apt-get install -y \
    build-essential \
    libasound2-dev \
    portaudio19-dev \
    libportaudio2 \
    libportaudiocpp0 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*
    
# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar o arquivo de dependências primeiro para otimizar o cache
COPY requirements.txt .

# Instalar as dependências de forma eficiente
RUN python -m pip install --upgrade pip && \
    pip install --default-timeout=1000 -r requirements.txt

# Baixar o modelo de linguagem SpaCy durante o build do container
RUN python -m spacy download pt_core_news_sm

# Copiar os arquivos restantes do projeto
COPY . .

# Expor a porta definida no .env ou uma porta padrão
ENV APP_PORT=5000
EXPOSE ${APP_PORT}

# Verificar e instalar o PyTorch apropriado (caso necessário)
RUN python -c "import torch" || \
    pip install torch==2.0.1+cpu --extra-index-url https://download.pytorch.org/whl/cpu

# Variável de ambiente para definir o aplicativo Flask
ENV FLASK_APP=flask_app.py
# Comando para rodar o Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
