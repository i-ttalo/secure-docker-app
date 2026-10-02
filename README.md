# Secure App

A security-focused multi-container application built with Docker Compose.

The project demonstrates container networking, service isolation, least privilege, health checks, resource limits, persistent storage, and failure troubleshooting using Nginx, Flask, and PostgreSQL.

## Architecture

```text
                         Host
                          |
                       :8080
                          |
                    +-----v-----+
                    |   Nginx   |
                    | Frontend  |
                    +-----+-----+
                          |
                  frontend-network
                          |
                    +-----v-----+
                    |   Flask   |
                    |  Backend  |
                    +-----+-----+
                          |
                   backend-network
                          |
                    +-----v-----+
                    | PostgreSQL|
                    | Database  |
                    +-----------+
                          |
                    postgres-data
```

Only the Nginx frontend is exposed to the host.

The Flask backend and PostgreSQL database communicate exclusively through internal Docker networks.

## Security Features

### Network segmentation

Two Docker bridge networks are used:

- `frontend-network`: communication between Nginx and Flask.
- `backend-network`: communication between Flask and PostgreSQL.

The frontend has no direct network path to the database.

### Non-root backend

The Flask application runs as a dedicated non-root user:

```dockerfile
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
```

### Read-only filesystem

The backend container uses:

```yaml
read_only: true
```

A temporary writable filesystem is provided only where needed:

```yaml
tmpfs:
  - /tmp
```

### Linux capabilities

All Linux capabilities are dropped from the backend:

```yaml
cap_drop:
  - ALL
```

The application does not require additional capabilities to serve HTTP on port 5000 or connect to PostgreSQL.

### Resource limits

The backend is restricted to:

```yaml
cpus: 0.50
mem_limit: 256m
```

This limits the impact of excessive resource consumption.

### Health checks

The Flask backend exposes:

- `/health` — application liveness.
- `/db-health` — verifies database connectivity.

PostgreSQL is checked using `pg_isready`.

Docker Compose waits for the database health check before starting the backend.

### Secrets and configuration

The PostgreSQL password is supplied through an environment variable.

The local `.env` file is excluded from Git:

```gitignore
.env
```

`.env.example` provides the required variable without committing the local value.

> `.env` is used for this lab and should not be considered a production secret-management solution.

## Failure Testing

The application was tested under service failure scenarios.

### Database unavailable

When PostgreSQL was stopped:

```text
/api/health     -> 200 OK
/api/db-health  -> 500 Internal Server Error
```

The Flask application remained alive while its database dependency was unavailable.

After PostgreSQL was restarted, database connectivity recovered without restarting the backend.

### Backend unavailable

When the Flask backend was stopped:

```text
/api/health -> 502 Bad Gateway
```

Nginx remained available but could not reach its upstream backend.

This demonstrates the distinction between an application error and an unavailable reverse-proxy upstream.

## Running the Project

### Requirements

- Docker
- Docker Compose

### Setup

Clone the repository and create the local environment file:

```bash
cp .env.example .env
```

Set a local password in `.env`:

```env
POSTGRES_PASSWORD=change-me
```

Build and start the application:

```bash
docker compose up -d --build
```

Check container status:

```bash
docker compose ps
```

Expected services:

```text
secure_frontend
secure_backend
secure_database
```

The backend and database should report healthy status.

## Testing

Frontend:

```bash
curl http://localhost:8080/
```

Backend health:

```bash
curl http://localhost:8080/api/health
```

Database connectivity:

```bash
curl http://localhost:8080/api/db-health
```

## Technology Stack

- Docker
- Docker Compose
- Nginx
- Python / Flask
- PostgreSQL

## Key Concepts Demonstrated

- Containerization
- Reverse proxy
- Docker DNS
- Network segmentation
- Least privilege
- Non-root containers
- Read-only filesystems
- Linux capability reduction
- Resource limits
- Persistent volumes
- Health checks
- Service dependencies
- Failure recovery
- Troubleshooting
