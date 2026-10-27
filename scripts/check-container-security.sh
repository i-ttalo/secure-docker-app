
#!/bin/sh
set -eu


CONTAINER="${1:-secure_backend}"

echo "[1/3] Checking non-root user..."

USER_ID=$(docker exec "$CONTAINER" id -u)

if [ "$USER_ID" = "0" ]; then
    echo "FAIL: Container is running as root"
    exit 1
fi

echo "PASS: Container uses UID $USER_ID"

echo "[2/3] Checking read-only filesystem..."

if docker exec "$CONTAINER" sh -c \
    'touch /app/security-check.txt' >/dev/null 2>&1; then
    docker exec "$CONTAINER" rm -f /app/security-check.txt
    echo "FAIL: Application directory is writable"
    exit 1
fi

echo "PASS: Application directory is protected"

echo "[3/3] Checking Linux capabilities..."

CAP_DROP=$(docker inspect "$CONTAINER" \
    --format '{{json .HostConfig.CapDrop}}')

if [ "$CAP_DROP" != '["ALL"]' ]; then
    echo "FAIL: Linux capabilities were not fully dropped"
    exit 1
fi

echo "PASS: All capabilities dropped"

echo "All container security checks passed!"