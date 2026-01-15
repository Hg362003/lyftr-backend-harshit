# Lyftr Backend Assignment – FastAPI Service

This repository contains a production-style backend service built using **FastAPI** as part of the **Lyftr AI Backend Assignment**. The application is designed to ingest WhatsApp-like webhook messages securely, ensure idempotent processing, and provide observability through health checks, analytics, and structured logging.

---

## Tech Stack
- Python
- FastAPI
- SQLite
- Docker & Docker Compose
- Pydantic

---

## Features
- Secure webhook ingestion using HMAC-SHA256 signature verification
- Idempotent message storage using database-level uniqueness
- Pagination, filtering, and search for stored messages
- Analytics endpoint for message statistics
- Liveness and readiness health checks
- Structured JSON logging
- Fully containerized setup following 12-factor principles

---

## Setup & Run

### Prerequisites
- Docker
- Docker Compose
- Make

### Environment Variables
```bash
export WEBHOOK_SECRET="testsecret"
export DATABASE_URL="sqlite:////data/app.db"
