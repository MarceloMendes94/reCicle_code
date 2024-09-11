# Use uma imagem base oficial do Python
FROM python:3.8

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de requirements para instalar as dependências
COPY requirements.txt /app/

# Instala as dependências listadas no requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante dos arquivos do projeto para o diretório de trabalho
COPY . /app/

# Expõe a porta que o Django usará (padrão é 8000)
EXPOSE 8000

# Comando para rodar a aplicação Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
