FROM python:3.13-alpine@sha256:83057c121ebd0ccd12511f81aeb7e3b36a36f81b9d0687f7b8fcc93935497768

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt \
    && python -m pip uninstall -y pip

COPY app.py .

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

USER appuser

CMD ["gunicorn", "--no-control-socket", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
