
# Secure App — Threat Model

## 1. System Overview

Secure App is a containerized application built with Docker Compose, Nginx, Flask, Gunicorn, and PostgreSQL.

The application demonstrates container isolation, network segmentation, least privilege, vulnerability scanning, and security controls.

## 2. Assets

| Asset | Security Objective |
|---|---|
| PostgreSQL credentials | Confidentiality |
| PostgreSQL database | Confidentiality, Integrity, Availability |
| Flask API | Integrity, Availability |
| Nginx reverse proxy | Integrity, Availability |
| Docker images | Integrity |
| GitHub repository and CI pipeline | Integrity |

## 3. Trust Boundaries

- External clients communicate with the Nginx frontend through port 8080.
- Nginx communicates with Flask through the frontend Docker network.
- Flask communicates with PostgreSQL through the backend Docker network.
- Database credentials are injected through environment variables.
- GitHub Actions builds and scans container images.

## 4. Threat Register

### THREAT-001 — Database Health Endpoint Abuse

**STRIDE Category:** Denial of Service

**Affected Asset:** Flask API and PostgreSQL availability

**Attack Surface:** `GET /api/db-health`

**Threat Description:**

An attacker sends excessive requests to the database health endpoint, causing repeated PostgreSQL connection attempts and potential resource exhaustion.

**Existing Controls:**

- Docker network segmentation
- Backend CPU and memory limits
- Non-root backend execution

**Mitigation Implemented:**

Nginx rate limiting:

- Rate: 5 requests per second per client IP
- Burst: 5
- Excess requests return HTTP 429
- Applied specifically to `/api/db-health`

**Validation:**

30 consecutive HTTP requests:

| HTTP Status | Count |
|---|---:|
| 200 OK | 7 |
| 429 Too Many Requests | 23 |

Nginx configuration validation completed successfully using `nginx -t`.

**Residual Risk:**

Rate limiting does not fully prevent distributed denial-of-service attacks. Requests from multiple source IPs and attacks targeting other endpoints may bypass this specific limit.

**Status:** Mitigated — residual risk remains.

## 5. Future Security Improvements

- Add automated Nginx configuration validation to CI.
- Improve secrets management.
- Evaluate TLS for external deployments.
- Expand request limiting where appropriate.
- Continue STRIDE analysis for other assets and trust boundaries.