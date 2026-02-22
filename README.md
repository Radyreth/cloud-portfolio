# Cloud Portfolio - CI/CD Pipeline

![CI/CD Pipeline](https://github.com/Radyreth/cloud-portfolio/actions/workflows/ci-cd.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)

> Pipeline CI/CD complet avec GitHub Actions : lint, tests, build Docker, scan de securite et deploiement automatique.

---

## Architecture

```
+-------------+     +------------------+     +----------------+
|             |     |                  |     |                |
|  Developer  +---->+  GitHub (main)   +---->+ GitHub Actions |
|  git push   |     |  Repository      |     | CI/CD Pipeline |
|             |     |                  |     |                |
+-------------+     +------------------+     +-------+--------+
                                                     |
                           +-------------------------+-------------------------+
                           |              |              |              |
                           v              v              v              v
                     +-----------+  +-----------+  +-----------+  +-----------+
                     |           |  |           |  |           |  |           |
                     |  Flake8   |  |  Pytest   |  |   Docker  |  |   Trivy   |
                     |  (Lint)   |  |  (Tests)  |  |  (Build)  |  |  (Scan)   |
                     |           |  |           |  |           |  |           |
                     +-----------+  +-----------+  +-----+-----+  +-----------+
                                                         |
                                                         v
                                                  +-------------+
                                                  |   ghcr.io   |
                                                  |  (Registry) |
                                                  +------+------+
                                                         |
                                                         v
                                                  +-------------+
                                                  |   Render    |
                                                  | (Deploy)    |
                                                  +-------------+
```

## Pipeline

```
 push / PR to main
        |
        v
  +--[LINT]--------+  Flake8 checks PEP8 compliance
        |
        v
  +--[TEST]--------+  Pytest runs 18 unit tests
        |
        v
  +--[BUILD]-------+  Docker build + push to ghcr.io
        |
        v
  +--[SCAN]--------+  Trivy detects vulnerabilities
        |
        v
  +--[DEPLOY]------+  Render webhook triggers deploy
```

## How it works

### 1. Code Quality (Lint)
**Flake8** analyzes the Python code to detect syntax errors, unused imports, and PEP8 style violations. If the code doesn't pass the lint step, the pipeline stops immediately — no point testing broken code.

### 2. Unit tests
**Pytest** runs 18 tests covering:
- HTTP responses for each endpoint (status codes)
- Calculator business logic (addition, subtraction, multiplication, division)
- Error cases (division by zero, missing parameters, invalid types)

### 3. Docker Build
The Docker image is built with `python:3.11-slim` to minimize size (~150MB vs ~900MB for the full image). It runs as a non-root user and uses Gunicorn as the production WSGI server.

### 4. Security scan
**Trivy** (by Aqua Security) scans the Docker image for CVEs (Common Vulnerabilities and Exposures) in system packages and Python dependencies.

### 5. Deployment
A Render webhook automatically triggers redeployment. The Render free tier is used (spins down after 15 min of inactivity).

## API Endpoints

| Method | Route        | Description                          |
|--------|-------------|--------------------------------------|
| GET    | `/`         | Home page listing available routes   |
| GET    | `/health`   | Health check for monitoring          |
| POST   | `/calculate`| JSON calculator                      |
| GET    | `/info`     | Environment info                     |

### Example request

```bash
curl -X POST http://localhost:5000/calculate \
  -H "Content-Type: application/json" \
  -d '{"a": 10, "b": 5, "operation": "add"}'

# Response: {"a": 10, "b": 5, "operation": "add", "result": 15}
```

## Run locally

```bash
# With Docker Compose
docker compose up --build

# Without Docker
pip install -r app/requirements.txt
python app/app.py

# Run tests
pip install pytest
pytest tests/ -v
```

## Render deployment setup

1. Create an account on [render.com](https://render.com) (free)
2. New > **Web Service** > connect this GitHub repo
3. Settings:
   - **Build Command**: `pip install -r app/requirements.txt`
   - **Start Command**: `gunicorn -w 2 -b 0.0.0.0:$PORT app.app:app`
4. Copy the **Deploy Hook** URL from Settings
5. In GitHub: Settings > Secrets > Actions > `RENDER_DEPLOY_HOOK` = the URL

## What I learned

Building this project taught me:

- **GitHub Actions**: YAML workflow syntax, jobs, steps, conditionals (`if`), and job dependencies (`needs`)
- **Docker**: layer cache optimization, slim images, non-root containers for security
- **CI/CD design**: why the Lint > Test > Build > Scan > Deploy order matters (fail fast principle)
- **DevSecOps**: scanning Docker images with Trivy to catch CVEs before deployment
- **Container registries**: publishing and versioning Docker images for free with ghcr.io
- **Continuous deployment**: using webhooks to trigger automatic deployments on Render

## Tech stack

| Tool            | Role                    | Cost |
|-----------------|-------------------------|------|
| Python/Flask    | API application         | Free |
| GitHub Actions  | CI/CD pipeline          | Free |
| Docker          | Containerization        | Free |
| Trivy           | Security scanning       | Free |
| ghcr.io         | Docker image registry   | Free |
| Render          | Hosting / Deployment    | Free |
| Flake8          | Python linter           | Free |
| Pytest          | Unit testing            | Free |

## License

MIT
