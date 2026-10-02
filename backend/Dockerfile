FROM python:3.13-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

USER appuser

CMD ["python", "app.py"]
