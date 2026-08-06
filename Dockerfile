FROM python:3.12-slim

RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

RUN mkdir -p /data && chown -R appuser:appuser /app /data

USER appuser

ENV PYTHONUNBUFFERED=1

EXPOSE 8090

CMD ["python", "-m", "app.main"]
