FROM python:3.10-slim

WORKDIR /app

# Install system dependencies if needed
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7860

# Ensure the server/ and env/ directories are in the Python path
ENV PYTHONPATH=/app

CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
