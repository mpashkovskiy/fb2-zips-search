FROM python:3.10-slim

RUN pip install --upgrade pip && \
    pip install pandas numpy fastapi uvicorn

WORKDIR /app
COPY static /app/static
COPY api.py /app
COPY index.json.zip /app/index.json.zip

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]