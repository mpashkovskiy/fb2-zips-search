FROM python:3.10-slim

RUN pip install --upgrade pip && \
    pip install fastapi uvicorn

WORKDIR /app
COPY static /app/static
COPY api.py /app
COPY index.json /app/index.json

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]