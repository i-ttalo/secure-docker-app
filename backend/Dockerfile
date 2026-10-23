FROM python:3.13-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

USER appuser

CMD ["gunicorn", "--no-control-socket", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
