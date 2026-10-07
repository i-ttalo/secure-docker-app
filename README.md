# Secure Docker App

Security-focused multi-container application built with Docker Compose using Nginx, Flask, and PostgreSQL.

The project demonstrates container isolation, network segmentation, least privilege, health checks, resource controls, persistent storage, and failure troubleshooting.

## Architecture

```text
                    Host :8080
                        |
                        v
                 +-------------+
                 |    Nginx    |
                 |  Frontend   |
                 +------+------+
                        |
                frontend-network
                        |
                 +------v------+
                 |    Flask    |
                 |   Backend   |
                 +------+------+
                        |
                 backend-network
                        |
                 +------v------+
                 | PostgreSQL  |
                 |  Database   |
                 +-------------+
                        |
                  postgres-data
```

Only the Nginx frontend is exposed to the host.

The backend and database remain internal and communicate through isolated Docker networks.

## Security Controls

| Control | Implementation |
|---|---|
| Network segmentation | Separate frontend and backend Docker networks |
| Service exposure | Only Nginx is published to the host |
| Non-root execution | Flask runs as a dedicated non-root user |
| Read-only filesystem | Backend filesystem is read-only with `/tmp` mounted as `tmpfs` |
| Linux capabilities | All backend capabilities are dropped |
| Resource limits | Backend limited to `0.50 CPU` and `256 MB` memory |
| Secret hygiene | Local `.env` excluded from Git |
| Service health | Application and database health checks |
| Persistent storage | PostgreSQL data stored in a Docker volume |

> `.env` is used for this lab and is not intended as a production secret-management solution.

## Health Checks

The Flask backend exposes:

```text
/health     -> application liveness
/db-health  -> PostgreSQL connectivity
```

PostgreSQL uses `pg_isready`, and Docker Compose waits for the database to become healthy before starting the backend.

## Failure Testing

The environment was intentionally tested under service failures.

| Scenario | Result |
|---|---|
| PostgreSQL unavailable | `/api/health` remained `200 OK` |
| PostgreSQL unavailable | `/api/db-health` returned `500` |
| PostgreSQL restarted | Database connectivity recovered |
| Flask backend unavailable | Nginx returned `502 Bad Gateway` |

These tests demonstrate the difference between application health, dependency health, and upstream availability.

## Run Locally

Requirements:

- Docker
- Docker Compose

Create the local environment file:

```bash
cp .env.example .env
```

Set a local PostgreSQL password:

```env
POSTGRES_PASSWORD=change-me
```

Start the application:

```bash
docker compose up -d --build
```

Check service status:

```bash
docker compose ps
```

Test the application:

```bash
curl http://localhost:8080/
curl http://localhost:8080/api/health
curl http://localhost:8080/api/db-health
```

## Technology 

**Containers:** Docker, Docker Compose  
**Frontend:** Nginx  
**Backend:** Python, Flask  
**Database:** PostgreSQL

