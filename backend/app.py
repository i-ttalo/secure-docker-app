import os

import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)


def get_db_connection():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
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

    except Exception as error:
        return jsonify(
            database="error",
            message=str(error)
        ), 500


@app.route("/")
def home():
    return jsonify(message="Secure App backend is running!")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

