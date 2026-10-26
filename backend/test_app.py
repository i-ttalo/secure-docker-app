
from unittest.mock import MagicMock

from backend import app as app_module

app = app_module.app


def test_health():
    client = app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json == {"status": "ok"}


def test_home():
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert response.json == {
        "message": "Secure App backend is running!"
    }


def test_db_connection_reads_secret(monkeypatch):
    fake_password = "test-password-not-real"

    monkeypatch.setenv("DB_HOST", "database")
    monkeypatch.setenv("DB_PORT", "5432")
    monkeypatch.setenv("DB_NAME", "secureapp")
    monkeypatch.setenv("DB_USER", "appuser")

    def fake_read_text(self):
        assert str(self) == "/run/secrets/db_password"
        return fake_password + "\n"

    monkeypatch.setattr(app_module.Path, "read_text", fake_read_text)

    fake_connection = MagicMock()

    def fake_connect(**kwargs):
        assert kwargs == {
            "host": "database",
            "port": "5432",
            "database": "secureapp",
            "user": "appuser",
            "password": fake_password,
        }
        return fake_connection

    monkeypatch.setattr(app_module.psycopg2, "connect", fake_connect)

    connection = app_module.get_db_connection()

    assert connection is fake_connection