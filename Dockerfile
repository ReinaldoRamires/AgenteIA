# Dockerfile
FROM python:3.11-slim

# 1. Define diretório de trabalho
WORKDIR /app

# 2. Instala dependências (cache-friendly)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copia todo o código
COPY . .

# 4. Ponto de entrada padrão: CLI do AgenteIA
ENTRYPOINT ["python", "src/main.py"]
CMD ["new-project", "--help"]
