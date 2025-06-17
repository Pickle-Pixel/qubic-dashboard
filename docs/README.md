# Qubic Grafana Dashboard

This documentation explains how the **Qubic Grafana Dashboard** works and how it helps visualize data from [pool.qubic.li](https://pool.qubic.li/en-US/dashboard) without needing to log in or do manual calculations.

## Why This Project Exists

The official Qubic dashboard requires a login and doesn't offer all the calculated values I want to see. To solve this, I built a local data collection and visualization pipeline that:
- Logs into my account automatically
- Fetches and stores key data points
- Makes calculated data visible at a glance
- Runs on my home server and is publicly viewable

## How It Works

1. **Credential Fetching**  
   Credentials are stored securely in AWS Secrets Manager.

2. **Login & Token Management**  
   A script logs into my Qubic account, retrieves the token, and refreshes it as needed.

3. **Data Fetching**  
   Using the token, data is pulled from the Qubic API, formatted as JSON, and saved in MongoDB.

4. **Local API Server**  
   A Flask server exposes the latest MongoDB data through a REST API on localhost.

5. **Grafana Dashboard**  
   Grafana uses the Infinity plugin to pull and visualize the data from the local API.

6. **Public Access**  
   The whole system is tunneled using Cloudflared and made accessible at:  
   👉 [Public Dashboard](https://grafana.pickle-pixel.com/public-dashboards/24a16f5501a64bf1a94cd0337c72301d)

---

## File Overview

### `credential_fetcher.py`
Fetches account credentials from AWS Secrets Manager securely.

### `qli_login.py`
Handles logging into Qubic, retrieving the access token, and refreshing it as needed.

### `data_fetcher.py`
Fetches account-specific metrics from the Qubic API using the token and saves them to MongoDB.

### `api_server.py`
Runs a local Flask server that reads from MongoDB and exposes the latest data as an API for Grafana to consume.

---

## Requirements
- Python 3.11+
- MongoDB (hosted or local)
- Flask
- Grafana with Infinity plugin
- Cloudflared (for public tunneling)
