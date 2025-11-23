# DevSecOps Pipeline Project

## Overview
This project demonstrates a complete DevSecOps CI/CD pipeline using Jenkins, SonarQube, Docker, and security scanning.

## Architecture
- **Application**: Python Flask REST API
- **CI/CD**: Jenkins Pipeline
- **Code Quality**: SonarQube
- **Security**: Trivy Scanner
- **Containerization**: Docker

## Pipeline Stages
1. **Checkout** - Pull code from repository
2. **Install Dependencies** - Install Python packages
3. **Unit Tests** - Run pytest with coverage
4. **Code Quality Analysis** - SonarQube scanning
5. **Quality Gate** - Ensure code meets standards
6. **Build Docker Image** - Create container image
7. **Security Scan** - Scan for vulnerabilities
8. **Deploy** - Run the application

## Local Development

### Prerequisites
- Python 3.11+
- Docker
- pip

### Setup
```bash
pip install -r requirements.txt
```

### Run Application
```bash
python app.py
```

### Run Tests
```bash
pytest tests/ -v --cov=.
```

### Build Docker Image
```bash
docker build -t devsecops-app .
docker run -p 5000:5000 devsecops-app
```

## API Endpoints
- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /api/users` - Get user list

## Author
DevOps Engineer Training Project
