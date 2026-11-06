<div align="center">

# 📈 Binance Futures Testnet Trading Bot

### A Structured Python CLI for Placing MARKET and LIMIT Orders (USDT-M)

*A clean, modular command-line trading bot with HMAC-SHA256 signed REST calls, strict input validation, rotating structured logs and layered error handling. It runs on the Binance Futures **Testnet**, so no real funds are involved.*



![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)




![Binance](https://img.shields.io/badge/Binance-Futures%20Testnet-F0B90B?logo=binance&logoColor=black)




![REST](https://img.shields.io/badge/API-REST%20%2B%20HMAC--SHA256-orange)



[📧 Hire Me](mailto:samarthworldwide@gmail.com) · [💼 LinkedIn](https://www.linkedin.com/in/samarth-shukla-b72003293) · [🐙 GitHub](https://github.com/Samarth7272)

</div>

---

## 📌 TL;DR (for recruiters)

- **What:** A Python CLI that places MARKET and LIMIT futures orders on Binance Futures Testnet (USDT-M).
- **Why it matters:** It shows how I work with a real exchange API: request signing, validation before any network call, structured logging and clear failure handling.
- **Deliberate design:** Built on raw REST calls (`requests` + HMAC-SHA256) rather than an SDK, so every request and response is fully visible and logged.
- **Safe to try:** Testnet only. No real money, and credentials are read from environment variables.

---

## 🎯 The Problem

Trading scripts are often one-file experiments with hard-coded keys, no validation and no logs. When an order fails, there is no way to tell why.

This project treats order placement like production software: validated inputs, signed requests, a reviewable audit trail, and failures that are classified and reported clearly.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🛒 **MARKET and LIMIT orders** | Place BUY or SELL orders from the command line |
| ✅ **Input validation** | Symbol, side, type and quantity are checked **before** any API call |
| 🔏 **Signed REST client** | Manual HMAC-SHA256 request signing, with no SDK dependency |
| 📝 **Structured logging** | Rotating log file (5 backups, 2 MB each) plus console output |
| 🔍 **Verbose mode (`-v`)** | DEBUG logs with full request and response payloads, including signed params |
| 🚦 **Layered error handling** | Input errors, Binance API errors and network errors are handled separately |
| 🔒 **Secrets via environment** | Keys are loaded from `.env`, never passed as CLI args or committed |
| 🧪 **Sample logs without credentials** | A mock script generates example logs with no API access |
| 🌐 **Testnet by default** | Mainnet is never used by default (`--base-url` can override) |

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3** | Core language |
| **requests** | HTTP client for the Binance REST API |
| **hmac / hashlib** | HMAC-SHA256 request signing |
| **argparse** | CLI interface |
| **python-dotenv** | Loading credentials from `.env` |
| **logging** (rotating handlers) | File and console logging |
| **Git & GitHub** | Version control |

---

## 🏗️ Architecture

```
        CLI  (cli.py · argparse)
                │
                ▼
     validators.py   ← validate symbol, side, type, quantity, price
                │
                ▼
        orders.py    ← order placement logic
                │
                ▼
        client.py    ← signed REST client (HMAC-SHA256)
                │
                ▼
   Binance Futures Testnet API
                │
                ▼
   SUCCESS / FAILURE result  +  logs/trading_bot.log
```

---

## 📁 Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py            # Signed REST client wrapper for Binance Futures
│   ├── orders.py            # Order placement logic (validation + client)
│   ├── validators.py        # CLI input validation
│   └── logging_config.py    # Logging setup (file + console handlers)
├── scripts/
│   └── generate_sample_logs.py   # Produces sample log files using a mock HTTP layer
├── logs/
│   ├── sample_market_order.log
│   └── sample_limit_order.log
├── cli.py                   # CLI entry point (argparse)
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🚀 Setup

### 1. Create a Binance Futures Testnet account

1. Go to [testnet.binancefuture.com](https://testnet.binancefuture.com).
2. Log in or register (you can sign in with a GitHub account).
3. Generate an **API Key** and **API Secret** from the testnet dashboard.
4. The testnet gives you a virtual USDT balance, so no real funds are involved.

### 2. Install dependencies

```bash
git clone https://github.com/Samarth7272/trading-bot-testnet.git
cd trading-bot-testnet

python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure credentials

```bash
cp .env.example .env
```

Fill in your testnet API key and secret in `.env`. The CLI loads it automatically on startup via `python-dotenv`, so no manual export is needed, and it works the same on Windows, macOS and Linux. Keep `.env` in the same folder as `cli.py`.

> 🔒 Credentials are read from environment variables rather than a config file or CLI flag, so secrets are never logged or committed. `.env` is gitignored.

> ℹ️ If you edit `.env` while a terminal is already open, close and reopen it (or re-activate your venv) so the new values are picked up.

---

## ▶️ How to Run

Run `python cli.py --help` to see all options.

### Place a MARKET order

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.002
```

### Place a LIMIT order

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.002 --price 100000
```

### Verbose logging (full request / response payloads, including signed params)

```bash
python cli.py --symbol ETHUSDT --side BUY --type MARKET --quantity 0.05 -v
```

Every run prints:

- an order request summary
- the order response (`orderId`, `status`, `executedQty`, `avgPrice` if available)
- a clear `SUCCESS` or `FAILURE` message

Logs are written to `logs/trading_bot.log` (INFO by default, DEBUG with `-v`), rotating with 5 backups of 2 MB each, and warnings and errors are also printed to the console.

---

## 🧾 Sample Logs

`logs/sample_market_order.log` and `logs/sample_limit_order.log` contain example output for one MARKET and one LIMIT order, generated with:

```bash
python scripts/generate_sample_logs.py
```

This script mocks the Binance HTTP layer, so it runs **without any API credentials or network access**. Real orders placed through `cli.py` log in the same format, with your real order IDs.

---

## 🧠 Design Decisions

- **Raw REST over `python-binance`:** implemented with `requests` and manual HMAC-SHA256 signing, so every request and response is fully visible for logging and there is no dependency on an SDK's testnet compatibility.
- **Order types:** MARKET and LIMIT are supported. LIMIT orders default to `GTC` (Good-Til-Canceled) time-in-force.
- **Symbol handling:** Binance's standard concatenated format (e.g. `BTCUSDT`) is expected, and input is validated and uppercased.
- **Credentials:** supplied through environment variables (see `.env.example`), not hard-coded or passed as CLI arguments, to avoid leaking secrets into shell history or logs.
- **Three failure classes, handled distinctly:**
  1. **Input validation errors**, caught before any API call.
  2. **Binance API errors** (4xx / 5xx with `code` / `msg` from the response body).
  3. **Network-level errors** (timeouts, connection failures).
  Each one is surfaced with a clear message and a non-zero exit code.
- **Testnet only:** the base URL defaults to `https://testnet.binancefuture.com`, and no mainnet endpoint is used by default (`--base-url` can override it).

---

## 🎓 Skills Demonstrated

- Integrating a **real financial exchange REST API**
- **HMAC-SHA256 request signing** and authenticated API calls
- Clean, **modular Python architecture** (client, orders, validators, logging)
- **Input validation** and defensive programming
- Production-style **logging** with rotation and verbosity levels
- **Error classification** and meaningful exit codes
- Secure **secret management** with environment variables
- Building a usable **CLI** with `argparse`
- Mocking external services to produce **reproducible sample output**

---

## 🔮 Roadmap

- [ ] 🛑 Stop-Limit and OCO order types
- [ ] 🖥️ Interactive CLI menu (`questionary` / `rich`)
- [ ] 🧪 Unit tests with `pytest` (mocked HTTP) and GitHub Actions CI
- [ ] 🔁 Retry with backoff for transient network errors
- [ ] 📊 Order history and position queries
- [ ] 🐳 Docker image

---

## ⚠️ Disclaimer

This project is for **educational and demonstration purposes** on the Binance Futures **Testnet**. It is not financial advice. Never commit API keys, and do not use mainnet credentials with this code without proper review and testing.

---

## 👨‍💻 About the Author

**Samarth Shukla** is a final-year B.Tech Computer Science student and Software Engineer Intern at LV8 Tech, working on REST API design, OAuth 2.0 and backend architecture for fintech integrations (Next.js, TypeScript, PostgreSQL).

**Skills:** JavaScript/TypeScript · React/Next.js · Node.js/Express · Python (FastAPI, Flask) · MongoDB · PostgreSQL · SQL · Docker · AWS · Git

### 💼 Open to Opportunities

I'm actively looking for **Software Engineer, Backend and Full-Stack** roles (full-time and internships). If this project caught your eye, I'd love to talk.

[

![Email](https://img.shields.io/badge/Email-samarthworldwide%40gmail.com-D14836?logo=gmail&logoColor=white)

](mailto:samarthworldwide@gmail.com)
[

![LinkedIn](https://img.shields.io/badge/LinkedIn-Samarth%20Shukla-0A66C2?logo=linkedin&logoColor=white)

](https://www.linkedin.com/in/samarth-shukla-b72003293)
[

![GitHub](https://img.shields.io/badge/GitHub-Samarth7272-181717?logo=github&logoColor=white)

](https://github.com/Samarth7272)

---

<div align="center">

⭐ If you found this project useful, please give it a star!

</div>
