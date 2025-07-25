# etapa 1: builder de dependências
FROM python:3.11-slim AS builder
WORKDIR /app

# 1) Copia apenas o requirements para cache de pip
COPY requirements.txt .

# 2) Instala dependências sem cache pip
RUN pip install --no-cache-dir -r requirements.txt

# etapa 2: imagem de runtime
FROM python:3.11-slim
WORKDIR /app

# 3) Transfere pacotes instalados e executáveis
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# 4) Copia restando do código
COPY . .

# 5) Definição de entrypoint e comando padrão
ENTRYPOINT ["python", "-m", "src.main"]
CMD ["--help"]
