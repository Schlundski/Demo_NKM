# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG UID=10001
RUN adduser --disabled-password --gecos "" --home "/home/appuser" --shell "/bin/sh" --uid "${UID}" appuser \
    && mkdir -p /home/appuser/.streamlit \
    && chown -R appuser:appuser /home/appuser /app

ENV HOME=/home/appuser

USER appuser

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]