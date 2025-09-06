FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Atualizar sistema (opcional, removido para evitar problemas de repositório)
# RUN apt-get update && apt-get upgrade -y

# Copiar arquivo de requirements
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar usuário não-root
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Comando padrão
CMD ["python", "mongodb_crud.py"]