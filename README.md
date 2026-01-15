# Lyftr Backend Assignment – FastAPI Service

This repository contains a production-style backend service built using FastAPI as part of the Lyftr AI Backend Assignment. The application securely ingests WhatsApp-like webhook messages, ensures idempotent processing, and provides observability through health checks, analytics, and structured logging.

## Tech Stack
- Python
- FastAPI
- SQLite
- Docker & Docker Compose

## Setup

### Environment Variables
export WEBHOOK_SECRET="testsecret"
export DATABASE_URL="sqlite:////data/app.db"

### Run
make up

## Endpoints
- POST /webhook
- GET /messages
- GET /stats
- GET /health/live
- GET /health/ready

## Setup Used
VS Code, Docker Desktop, Git, and AI-assisted guidance.
