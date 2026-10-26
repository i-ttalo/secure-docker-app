
import os
from pathlib import Path

import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)


def get_db_connection():
    password = Path("/run/secrets/db_password").read_text().strip()

    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=password,
    )


@app.route("/health")
def health():
    return jsonify(status="ok")


@app.route("/db-health")
def db_health():
    try:
        conn = get_db_connection()
        conn.close()

        return jsonify(database="connected")

    except psycopg2.OperationalError:
        return jsonify(
            database="error",
            message="Database unavailable",
        ), 500


@app.route("/")
def home():
    return jsonify(message="Secure App backend is running!")