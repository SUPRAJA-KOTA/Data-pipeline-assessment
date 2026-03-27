# Data-pipeline-assessment
# Data Pipeline Assessment

## Overview

This project implements a containerized data pipeline using Flask, FastAPI, and PostgreSQL.

Flow:
Flask (Mock API) → FastAPI (Ingestion Service) → PostgreSQL → API Response

The Flask service provides mock customer data, which is ingested by the FastAPI service and stored in PostgreSQL. The stored data can then be queried via API endpoints.

---

## Tech Stack

* Flask (Mock API)
* FastAPI (Pipeline Service)
* PostgreSQL (Database)
* Docker & Docker Compose
* SQLAlchemy

---

## How to Run

### Prerequisites

* Docker Desktop installed and running
* Docker Compose

### Start Services

```
docker compose up -d --build
```

---

## Services

* Flask Mock Server → http://localhost:5000
* FastAPI Service → http://localhost:8000
* FastAPI Docs → http://localhost:8000/docs

---

## API Endpoints

### Flask (Mock Server)

* GET `/api/health`
* GET `/api/customers?page=1&limit=5`
* GET `/api/customers/{id}`

---

### FastAPI (Pipeline Service)

* POST `/api/ingest`
  → Fetches data from Flask and stores in PostgreSQL

* GET `/api/customers?page=1&limit=5`
  → Returns paginated customers from database

* GET `/api/customers/{id}`
  → Returns single customer

---

## Testing

### 1. Check Flask API

```
curl http://localhost:5000/api/health
```

```
curl "http://localhost:5000/api/customers?page=1&limit=5"
```

---

### 2. Run Ingestion Pipeline

```
curl -X POST http://localhost:8000/api/ingest
```

---

### 3. Fetch Data from FastAPI

```
curl "http://localhost:8000/api/customers?page=1&limit=5"
```

---

## Features

* JSON-based mock data source
* Pagination support
* RESTful APIs
* Data ingestion pipeline
* PostgreSQL storage
* Upsert logic (avoids duplicates)
* Fully Dockerized setup

---

## Notes

* Flask loads customer data from a JSON file
* FastAPI handles ingestion and database operations
* PostgreSQL is used as the persistent data store
* Services communicate using Docker networking

---

## Author

Supraja
