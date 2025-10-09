FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir flask python-dotenv

EXPOSE 8080

CMD ["python", "app.py"]
