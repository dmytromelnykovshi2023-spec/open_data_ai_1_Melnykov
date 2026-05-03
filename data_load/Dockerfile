FROM --platform=linux/amd64 python:3.10-slim
WORKDIR /app
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# 1. Копіюємо файл, який називається просто requirements
COPY requirements .

# 2. Читаємо бібліотеки з файлу requirements
RUN pip install --no-cache-dir -r requirements

COPY . .
CMD ["python", "app.py"]