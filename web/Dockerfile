FROM --platform=linux/amd64 python:3.10-slim
WORKDIR /app
COPY requirements .
RUN pip install --no-cache-dir -r requirements
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]