FROM python:3.12-slim

# Evita que o Python gere arquivos .pyc e não bufferize stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instala dependências do sistema necessárias para o OpenCV e o wget
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Instala pacotes Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia todo o código do projeto para o container
COPY . /app/

# Cria o diretório de armazenamento e o de modelos (caso não existam)
RUN mkdir -p /app/storage/images /app/app/models

# Baixa o modelo original do Haar Cascade (evita ter que gerenciar o XML manualmente)
RUN wget https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml -O /app/app/models/haarcascade_frontalface_default.xml

# Exposição da porta de comunicação da API
EXPOSE 8000

# Inicializa o Uvicorn apontando para a raiz do projeto copiado
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
