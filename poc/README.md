# Monitoring System POC for Nooxit

This repository contains a Proof of Concept (POC) for monitoring Nooxit’s system using Prometheus and Grafana. The system collects and visualizes metrics such as availability, model correctness, and banking statement processing rates.

## Features

- **Metrics Collection:** Python workers exposing metrics through Prometheus.
- **Docker Deployment:** Deploy with docker
- **Prometheus Integration:** Metrics scraping and aggregation with Victoria Metrics
- **Grafana Dashboards:** Real-time visualization for internal, customer, and public stakeholders.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Grafana Dashboards](#dashboards)
4. [Metrics](#metrics)
---

## Prerequisites

1. **Tools:**
   - Docker

---

## Installation

### 1. Clone the Repository
```bash
   git clone https://github.com/derhnyel/nooxit-monitoring-poc.git
   cd nooxit-monitoring-poc
```

### 2. Start the services
```bash
  cd poc
  docker compose up --build --force-recreate -d
```

### 3. Visit Dashboard Link 
* **Note** : The promql queries and Dashboard files can be found in the /grafana/src/dashboard directory
* Access Grafana at http://localhost:3000 (default credentials: nooxit/nooxit).
* Navigate to the Dashboard Tab

## Dashboards
1. Personalized Dashboard
	•	Number of banking statements processed per minute.
	•	Error rate of processed transactions.
	•	Model correctness rate.
	•	Open positions remaining.

2. Public Status Page
	•	System availability.
	•	AI correctness over time.

3. Internal Dashboard
	•	Worker metrics: success vs failure rates.
	•	Resource usage: CPU, memory, network throughput.
	•	Dependency insights: open positions reused, ERP API response rates.

## Metrics
Key Metrics Exposed by Workers
	•	Banking Statements Processed:
   ```json
   rate(statements_processed_total[1m])
   ```
   •	Error Rate:
   ```json
   rate(statements_processed_total[1m])
   ```
   •	Model Correctness:
   ```json
   avg(model_correctness_ratio)
   ```
   •	Open Positions:
   ```json
   avg(open_positions)
   ```
   • Memory and Cpu Usage



