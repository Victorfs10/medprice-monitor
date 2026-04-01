# Medprice-monitor

A Python REST API for monitoring and tracking medication prices across Brazilian pharmacies.


## Overview

The Medprice-monitor project collects and stores price data from pharmacy websites, allowing you to track price history per product and per store. Scraping is orchestrated by an external **n8n** workflow that triggers the API on a schedule — and in the future will also send price alerts via WhatsApp and email.

## Stack

| Layer | Technology |
|---|---|
| Web framework | Flask |
| Database | PostgreSQL |
| DB driver | psycopg2-binary |
| HTTP / Scraping | requests |
| Package manager | UV |
| Workflow orchestration | n8n |

## Architecture

The project follows a layered architecture with strict separation of concerns.

```
medprice-monitor/
├── main.py                        # Flask entry point
├── config.py                      # Configuration (DB, env vars)
└── app/
    ├── api/
    │   ├── prices.py              # GET /precos, GET /precos/<id>
    │   └── scraper.py             # POST /scrape/<farmacia>
    ├── services/
    │   ├── price_service.py       # Price query logic
    │   └── scraper_service.py     # Scraper orchestration and persistence
    ├── repositories/
    │   └── price_repository.py    # SQL queries
    ├── scrapers/
    │   └── base_scraper.py        # Base class (interface)
    ├── db/
    │   └── connection.py          # PostgreSQL connection
    └── __init__.py
```

### Data flow

```
n8n (cron) → POST /scrape/<farmacia> → scraper_service → Scraper → PostgreSQL
                                                                          ↓
             n8n (future) → GET /precos → notify via WhatsApp / Email ←──┘
```

## Getting Started

### Prerequisites

- Python 3.11+
- [UV](https://github.com/astral-sh/uv)
- Docker (for PostgreSQL)

### 1. Clone the repository

```bash
git clone https://github.com/Victorfs10/medprice-monitor.git
cd medprice-monitor
```

### 2. Set up environment variables

Create a `.env` file in the project root:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=medprice_monitor
DB_USER=postgres
DB_PASSWORD=your_password
```

### 3. Start PostgreSQL

```bash
docker run --name postgres-medprice \
  -e POSTGRES_PASSWORD=your_password \
  -e POSTGRES_DB=medprice_monitor \
  -p 5432:5432 \
  -d postgres
```

### 4. Create the database schema

```sql
CREATE TABLE produtos (
    id SERIAL PRIMARY KEY,
    nome TEXT,
    ean VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE precos (
    id SERIAL PRIMARY KEY,
    produto_id INTEGER REFERENCES produtos(id),
    preco NUMERIC(10,2),
    farmacia TEXT,
    url TEXT,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 5. Install dependencies and run

```bash
uv sync
uv run python main.py
```

The API will be available at `http://localhost:5000`.

## API Endpoints

### Get all prices

```http
GET /precos
```

Returns the 100 most recent price records.

### Get price by ID

```http
GET /precos/<id>
```

### Trigger scraping

```http
POST /scrape/<farmacia>
Content-Type: application/json

{
  "query": "dipirona"
}
```

**Supported pharmacies:**

| Key | Pharmacy |
|---|---|
| `drogaria_sao_paulo` | Drogaria São Paulo |

**Response:**

```json
{
  "scraped": 42,
  "saved": 40
}
```

## N8n Integration

Scraping is triggered by an n8n workflow running on a schedule. The workflow calls `POST /scrape/<farmacia>` with the desired search query. Future workflows will also call `GET /precos` and dispatch price alerts via WhatsApp and email.

To expose a local instance to n8n, you can use [ngrok](https://ngrok.com):

```bash
ngrok http 5000
```

Then point your n8n HTTP Request node to the generated URL.

## Adding a New Scraper

1. Create a new file under `app/scrapers/` (e.g., `farmacia_xyz_scraper.py`)
2. Inherit from `BaseScraper` and implement the `scrape(query: str) -> list[dict]` method
3. Register the scraper in `scraper_service.py` under the `SCRAPERS` dict

Each scraper should return a list of dicts with the following fields:

```python
{
    "nome": str,
    "ean": str,
    "preco": float,
    "preco_lista": float,
    "farmacia": str,
    "url": str,
    "disponivel": bool,
}
```

## Roadmap

- [x] Drogaria São Paulo scraper
- [ ] Price alert notifications (WhatsApp / Email)
- [ ] More pharmacy sources
- [ ] Price history charts
