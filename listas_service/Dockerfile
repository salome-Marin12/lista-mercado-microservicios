FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8002

# PRODUCTS_SERVICE_URL se inyecta desde docker-compose o Render
ENV PRODUCTS_SERVICE_URL=http://productos-service:8001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
