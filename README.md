# Qubic Dashboard

Automated data pipeline that collects mining performance metrics from the Qubic blockchain pool, stores them in MongoDB, and visualizes them through Grafana dashboards.

Public dashboard: [grafana.pickle-pixel.com](https://grafana.pickle-pixel.com/public-dashboards/24a16f5501a64bf1a94cd0337c72301d)

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────┐     ┌─────────┐     ┌──────────┐
│ Qubic Pool  │────►│ Data Fetcher │────►│ MongoDB │────►│ Flask   │────►│ Grafana  │
│ API (3 endpoints) │ (every 5min) │     │ Atlas   │     │ API     │     │ Dashboard│
└─────────────┘     └──────────────┘     └─────────┘     └─────────┘     └──────────┘
       │                    │                                                   │
  Cloudflare          JWT auth +                                         Cloudflared
  protected           token refresh                                      public tunnel
```

## Tech Stack

| Layer | Tools |
|---|---|
| Data Collection | Python, JWT authentication, token auto-refresh, Cloudflare bypass (tls_requests) |
| Storage | MongoDB Atlas (time-series metrics) |
| API | Flask REST server, JSON responses |
| Visualization | Grafana + Infinity plugin, public dashboards |
| Security | AWS Secrets Manager (credentials), JWT token management |
| Infrastructure | Cloudflared tunneling, cron scheduling, Linux deployment |

## Data Points Collected

Every 5 minutes, the pipeline fetches and stores:

| Metric | Source |
|---|---|
| Active connections | Pool user API |
| Total shares | Pool user API |
| Shares per solution | Pool user API |
| Epoch number | Pool user API |
| Qubic per solution (100%/95%/90%) | Revenue estimation API |
| Total pool hashrate | Dashboard stats API |
| Qubic price (USD) | CoinPaprika API |
| Computed: total solutions | `total_shares / shares_per_solution` |

## Project Structure

```
qubic-dashboard/
├── main.py               # Entry point — runs data collection loop (every 5 min)
├── data_fetcher.py       # Qubic API client + MongoDB storage
├── qli_login.py          # JWT authentication with auto-refresh
├── api_server.py         # Flask API serving latest metrics to Grafana
├── credential_fetcher.py # AWS Secrets Manager integration
├── requirements.txt
└── docs/                 # Docsify documentation site
```

## Setup

```bash
pip install -r requirements.txt
```

Requires:
- AWS credentials configured for Secrets Manager
- MongoDB Atlas connection (or local MongoDB)
- Grafana with Infinity plugin installed

### Run

```bash
# Start data collection (runs continuously, fetches every 5 min)
python main.py

# Start API server for Grafana (separate process)
python api_server.py
```

### Grafana Configuration

1. Install the Infinity data source plugin
2. Add a JSON data source pointing to `http://localhost:5001/data`
3. Build panels using the collected metrics
