
from pathlib import Path

import yaml

compose_path = Path("compose.yaml")
compose = yaml.safe_load(compose_path.read_text())

backend = compose["services"]["backend"]

assert backend.get("read_only") is True, (
    "Backend must use a read-only root filesystem"
)

assert backend.get("cap_drop") == ["ALL"], (
    "Backend must drop all Linux capabilities"
)

assert "/tmp" in backend.get("tmpfs", []), (
    "Backend must provide a temporary writable directory"
)

assert "db_password" in backend.get("secrets", []), (
    "Backend must use the database password secret"
)

print("PASS: Docker Compose backend security controls verified")