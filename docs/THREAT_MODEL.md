
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



### THREAT-002 — Database Credential Exposure

**STRIDE Category:** Information Disclosure

**Affected Asset:** PostgreSQL credentials

**Attack Surface:**
- Docker container environment variables
- Local configuration files
- Docker daemon and host filesystem access

**Threat Description:**

An attacker with sufficient access to Docker container metadata or local configuration files may obtain database credentials.

**Initial Finding:**

The backend and database containers exposed their passwords through environment variables inspectable with Docker.

**Mitigation Implemented:**

- Migrated credentials to Docker Compose Secrets.
- Configured Flask to read `/run/secrets/db_password`.
- Configured PostgreSQL with `POSTGRES_PASSWORD_FILE`.
- Removed password values from container environment variables.
- Excluded the local `secrets/` directory from Git.
- Mounted the secret as read-only.
- Applied restricted filesystem permissions and ACLs.

**Validation:**

- `DB_PASSWORD` absent from backend container metadata.
- `POSTGRES_PASSWORD` absent from database container metadata.
- `POSTGRES_PASSWORD_FILE` configured.
- Secret mounted with `RW=false`.
- Secret reading verified from an authorized execution context.
- `/api/db-health` returned HTTP 200.
- PostgreSQL remained operational with persistent data.

**Known Limitation:**

Direct reading of the bind-mounted secret as UID 70 failed in an isolated container test, despite a host ACL. The PostgreSQL image's normal startup path remained functional.

**Residual Risk:**

Docker Compose file-backed secrets are not a dedicated encrypted secret-management service.

Administrators with sufficient Docker or host access may still retrieve the secret. Local filesystem ACLs and UID mappings can behave differently across environments.

**Status:** Partially mitigated — residual risk remains.


## THREAT-003 — Software Supply Chain Compromise

**STRIDE Category:** Tampering

### Threat Description

An attacker could compromise a base Docker image or a software
dependency used during the application's build process.

Mutable image tags and unverified dependencies may introduce
unexpected or malicious components into production images.

### Affected Assets

- Backend Docker image
- Frontend Docker image
- Python dependencies
- CI/CD build pipeline

### Implemented Mitigations

1. Docker base images are pinned using SHA-256 digests.
2. Trivy scans backend and frontend images for HIGH and
   CRITICAL vulnerabilities during CI.
3. pip-audit checks Python dependencies.
4. CycloneDX SBOMs are automatically generated in CI.
5. SBOMs are retained as GitHub Actions artifacts for 30 days.

### Verification

- Both Docker images build successfully using pinned digests.
- Trivy identified no HIGH or CRITICAL vulnerabilities
  in the tested images.
- GitHub Actions completed successfully.
- Backend and frontend SBOM generation succeeded.

### Residual Risks

- Pinned images do not receive updates automatically.
- Vulnerability scanners cannot identify every security issue.
- SHA-256 pinning does not independently verify image provenance.
- Python dependencies are not yet fully locked.
- Third-party GitHub Actions are not yet pinned by commit SHA.

### Maintenance Policy

- Review base-image updates at least monthly.
- Update image digests when security fixes are released.
- Run all CI security checks after dependency updates.
- Review newly disclosed vulnerabilities affecting the SBOM components.
