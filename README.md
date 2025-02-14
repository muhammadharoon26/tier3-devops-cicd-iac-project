# Tier3 DevOps CICD IAC Project
A DevOps project showcasing version control, automated testing, CI/CD, containerization, monitoring, and infrastructure as code.

First, let's create the project structure. Here's what we'll use:
- GitHub (free account) for source control
- GitHub Actions for CI/CD
- Prometheus + Grafana Cloud (free tier) for monitoring
- Python Flask for the web application
- Docker for containerization
- Render.com (free tier) for hosting

```text
devops-project/
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── metrics.py
├── tests/
│   ├── __init__.py
│   └── test_app.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md

```

Let's create each component step by step:

1. First, the Flask application with Prometheus metrics:

```python
# app/main.py
from flask import Flask, Response
from prometheus_client import generate_latest
from .metrics import request_count, request_latency

app = Flask(__name__)

@app.route('/')
def hello_world():
    request_count.inc()
    return 'Hello, DevOps World!'

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# app/metrics.py
from prometheus_client import Counter, Histogram

request_count = Counter(
    'app_request_count',
    'Total number of requests to the web application'
)

request_latency = Histogram(
    'app_request_latency_seconds',
    'Request latency in seconds'
)

```

2. Create the tests:

```python
# tests/test_app.py
import pytest
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_hello_world(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Hello, DevOps World!' in response.data

def test_metrics_endpoint(client):
    response = client.get('/metrics')
    assert response.status_code == 200
    assert b'app_request_count' in response.data

```

3. Set up Docker:

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "-m", "app.main"]

# docker-compose.yml
version: '3'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    restart: always

```

4. Create the requirements file:

```text
Flask==2.0.1
prometheus-client==0.11.0
pytest==6.2.5
gunicorn==20.1.0

```

5. Set up GitHub Actions for CI/CD:

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run tests
      run: |
        pytest

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Deploy to Render
      run: |
        echo "Deploy by creating a deploy hook in Render.com and calling it here"
      # Add the actual deploy command once you set up Render

```

Now, let's go through the setup process:

1. Create a GitHub repository and push the code:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main
```

2. Set up Render.com:
   - Create a free account on Render.com
   - Create a new Web Service
   - Connect your GitHub repository
   - Set the following:
     - Runtime: Docker
     - Build Command: `docker build -t app .`
     - Start Command: `docker run -p 5000:5000 app`

3. Set up Grafana Cloud free tier:
   - Sign up for Grafana Cloud free tier
   - Get your Prometheus endpoint and API key
   - Add the following environment variables to your Render.com service:
     - PROMETHEUS_ENDPOINT
     - PROMETHEUS_API_KEY

4. Testing locally:
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest

# Run the application
python -m app.main

# Build and run with Docker
docker-compose up --build
```

The project demonstrates several DevOps practices:
- Version Control (GitHub)
- Automated Testing (pytest)
- CI/CD (GitHub Actions)
- Containerization (Docker)
- Monitoring (Prometheus)
- Infrastructure as Code (docker-compose)

Some advanced features you can add:
1. Add more metrics in `metrics.py`
2. Create Grafana dashboards
3. Add API rate limiting
4. Implement caching
5. Add error tracking
