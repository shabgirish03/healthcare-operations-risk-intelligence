# Hospital Models API — Deployment & Operations Runbook

## Overview

This document describes the deployment, configuration, and operational management of the Hospital Models API.

The API exposes two machine learning models:

- **Risk Classification Model**
  - Predicts patient visit risk level: Low, Medium, High
  - Used by hospital operations teams for resource allocation
- **Claim Outcome Classification Model**
  - Predicts claim status: Paid, Pending, Rejected
  - Used by finance and billing teams

The service is built using FastAPI, containerized using Docker, and designed for real-time prediction.

## Architecture Overview

```
Hospital System / Dashboard
            ↓
     FastAPI Service
            ↓
Risk Model (.pkl)    Claim Model (.pkl)
```

FastAPI handles request validation, prediction calls, logging, and response formatting. Models are loaded at startup.

> **Note:** The `.pkl` model files are not included in this repository. Run `notebooks/03_modelling.ipynb` to generate `risk_model.pkl` and `claim_rf_model.pkl`, then place them in the same folder as `app.py`.

## System Requirements

- Python 3.12+
- Docker (for containerized deployment)
- Minimum 2GB RAM recommended

## Local Deployment (Without Docker)

**Step 1: Install dependencies**

```bash
pip install -r requirements.txt
```

**Step 2: Run the API server**

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

**Step 3: Verify the health check**

Open in a browser: `http://localhost:8000/health`

Expected response:

```json
{
  "status": "OK",
  "timestamp": "2026-02-26T10:20:30.123Z"
}
```

## Docker Deployment

**Step 1: Build the Docker image**

```bash
docker build -t hospital-ai-api:latest .
```

**Step 2: Run the container**

```bash
docker run -d -p 8000:8000 hospital-ai-api:latest
```

**Step 3: Verify the container is running**

```bash
docker ps
```

## API Endpoints

### Health Check

`GET /health`

```json
{
  "status": "OK",
  "timestamp": "2026-02-26T10:20:30.123Z"
}
```

### Risk Prediction

`POST /predict/risk`

Sample request:

```bash
curl -X POST "http://localhost:8000/predict/risk" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 45,
    "gender": "M",
    "chronic_flag": 1,
    "city": "CityA",
    "department": "ER",
    "visit_type": "OPD",
    "length_of_stay_hours": 12.5,
    "visit_frequency": 3,
    "avg_length_of_stay": 10,
    "provider_rejection_rate": 0.05,
    "days_since_registration": 300,
    "visit_month": 2,
    "visit_weekday": 3
  }'
```

Sample response:

```json
{
  "risk_score": "High",
  "timestamp": "2026-02-26T10:22:10.567Z"
}
```

### Claim Prediction

`POST /predict/claim`

Sample request:

```bash
curl -X POST "http://localhost:8000/predict/claim" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 45,
    "gender": "M",
    "chronic_flag": 1,
    "city": "CityA",
    "department": "ER",
    "visit_type": "OPD",
    "length_of_stay_hours": 12.5,
    "billed_amount": 500,
    "approved_amount": 450,
    "payment_days": 30,
    "visit_frequency": 3,
    "avg_length_of_stay": 10,
    "provider_rejection_rate": 0.05,
    "days_since_registration": 300,
    "visit_month": 2,
    "visit_weekday": 3
  }'
```

Sample response:

```json
{
  "claim_status": "Paid",
  "timestamp": "2026-02-26T10:25:40.111Z"
}
```

## Request & Response Validation

Request and response validation is important to make sure the API only accepts proper and expected data. In this project, Pydantic is used to handle validation, as it checks whether the input data matches the structure defined in the schema.

Pydantic automatically checks data types like integers, floats, and strings. So if a field expects an integer and someone sends a string instead, it will raise an error.

If the request data is invalid or does not match the schema, the API returns an HTTP 422 error. This means the server understands the request, but the data provided is incorrect or incomplete.

Overall, validation helps keep the system stable and prevents unexpected errors by ensuring only properly formatted data is processed.

## Logging & Monitoring

Each prediction logs:

- Timestamp (UTC)
- Prediction result
- Input feature hash (MD5)
- Model version (if implemented)

## Security Considerations

> **Current status:** this API is a demo and has **no authentication**. It is not intended for production use or for real patient data.

Security is a very important aspect of APIs, especially when the system handles sensitive information like patient data.

First, the API should not be exposed publicly without proper authentication. If anyone can access it without verifying their identity, it can lead to data leaks. Adding an extra layer of protection makes sure only authorized users can use the API.

In production, HTTPS should always be used instead of HTTP, because it encrypts data sent between the client and the server. Even if someone intercepts the data, they won't be able to easily read it.

Access should also be restricted using API keys, which help identify and control who is using the API. Firewall rules can additionally limit which IP addresses can reach the server. Both add extra layers of protection.

Finally, sensitive patient information should not be logged. Logs are useful for debugging, but if they contain private patient information they become a security and privacy issue. It is better to log only necessary technical details and not confidential data.
