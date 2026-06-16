# ⚡ OpsPulse: Asynchronous Service Monitor & Alerting Engine

A lightweight, high-performance monitoring service built with Python and AsyncIO. OpsPulse continuously tracks the health of your web applications, APIs, and services, sending instant Telegram alerts if any endpoints experience downtime, latency spikes, or unexpected HTTP status codes.

## 🚀 Features

- **Asynchronous Polling:** Leverages `httpx` and `asyncio` to monitor dozens of endpoints concurrently without blocking.
- **Smart State Tracking:** Prevents alert spam by tracking the exact state of each service. You get exactly one alert when a service goes down, and one when it recovers.
- **Redirect Handling:** Automatically resolves HTTP 301/302 redirects to check the true destination state.
- **Docker Ready:** Includes multi-container orchestration setup (`docker-compose`) for seamless deployment to VPS.

## 🛠 Tech Stack
* **Language:** Python 3.10+
* **Concurrency:** Asyncio, HTTPX
* **Notifications:** Telegram Bot API
* **Deployment:** Docker, Docker Compose

## 📋 Quick Start (Local Setup)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/derraain/opspulse.git