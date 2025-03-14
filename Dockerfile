FROM python:3.12-slim

# Instala dependências de sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libmariadb-dev-compat libmariadb-dev pkg-config && \
    rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho
WORKDIR /app

# Copia o arquivo de dependências
COPY requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Expõe a porta 5000
EXPOSE 5000

# Define variáveis de ambiente
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV FLASK_RUN_HOST=0.0.0.0

# Comando padrão para rodar o Flask
CMD ["flask", "run"]