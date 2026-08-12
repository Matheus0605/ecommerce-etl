# Dockerfile for the ETL app + Streamlit
FROM python:3.11-slim

WORKDIR /app

# system deps for psycopg2
RUN apt-get update \
    && apt-get install -y build-essential default-libmysqlclient-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8501

CMD ["streamlit","run","src/dashboard/quality_dashboard.py","--server.port","8501","--server.address","0.0.0.0"]
