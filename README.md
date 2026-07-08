## Simplified Trading Bot — Binance Futures Testnet (USDT-M)

A small, structured Python CLI application for placing MARKET and LIMIT
orders on Binance Futures Testnet, with input validation, structured
logging, and clean error handling.

## Project Structure

```
trading_bot/
  bot/
    __init__.py
    client.py          # Signed REST client wrapper for Binance Futures Testnet
    orders.py           # Order placement logic (validation + client + result formatting)
    validators.py        # CLI input validation
    logging_config.py    # Logging setup (file + console handlers)
  scripts/
    generate_sample_logs.py  # Produces sample log files with a mocked API (no credentials needed)
  logs/
    sample_market_order.log
    sample_limit_order.log
  cli.py                # CLI entry point (argparse)
  requirements.txt
  .env.example
  README.md
```

## Setup

### 1. Create a Binance Futures Testnet account
1. Go to https://testnet.binancefuture.com
2. Log in / register (you can use a GitHub account to sign in).
3. Once logged in, generate an **API Key** and **API Secret** from the
   testnet dashboard (top right → API Key).
4. The testnet gives you a virtual USDT balance automatically for placing
   orders — no real funds are involved.

### 2. Install dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure credentials
Copy `.env.example` to `.env` and fill in your testnet API key/secret:
```bash
cp .env.example .env
```
The CLI automatically loads `.env` on startup via `python-dotenv` — no
manual export needed, and this works the same on Windows, macOS, and Linux.
Just make sure `.env` sits in the same folder as `cli.py`.

The app deliberately reads credentials from environment variables rather
than a config file or CLI flag, so secrets are never logged or committed
to source control (`.env` is gitignored).

> **Note:** if you edit `.env` while a terminal is already open, close and
> reopen the terminal (or re-activate your venv) so the new values are
> picked up on the next run.

## How to Run

### Place a MARKET order
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

### Place a LIMIT order
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 65000
```

### Verbose logging (full request/response payloads, incl. signed params)
```bash
python cli.py --symbol ETHUSDT --side BUY --type MARKET --quantity 0.5 -v
```

Every run prints:
- an order request summary
- the order response (`orderId`, `status`, `executedQty`, `avgPrice` if
  available)
- a clear `SUCCESS` / `FAILURE` message

Logs (INFO by default, DEBUG with `-v`) are written to `logs/trading_bot.log`
(rotating, 5 backups, 2MB each) as well as printed to console for
warnings/errors.

### Sample logs
`logs/sample_market_order.log` and `logs/sample_limit_order.log` contain
example log output for one MARKET and one LIMIT order, generated via:
```bash
python scripts/generate_sample_logs.py
```
This script mocks the Binance HTTP layer so it can be run without any API
credentials or network access, purely to demonstrate logging output for
the assignment deliverable. Actual orders placed via `cli.py` against the
real testnet will log the same way (with your real order IDs).

## Design Notes / Assumptions

- **REST calls over python-binance**: implemented with `requests` and
  manual HMAC-SHA256 signing rather than the `python-binance` SDK, so
  every request/response is fully visible for logging purposes and there's
  no dependency on the SDK's testnet compatibility at any given version.
- **Order types**: only `MARKET` and `LIMIT` are required; `LIMIT` orders
  default to `GTC` (Good-Til-Canceled) time-in-force since the task didn't
  specify one.
- **Symbol format**: assumed to be Binance's standard concatenated format,
  e.g. `BTCUSDT`, and is validated/uppercased accordingly.
- **Credentials**: assumed to be supplied via environment variables (see
  `.env.example`) rather than hardcoded or passed as CLI args, to avoid
  leaking secrets into shell history or logs.
- **Error handling**: three failure classes are handled distinctly —
  input validation errors (caught before any API call), Binance API errors
  (4xx/5xx with `code`/`msg` from the response body), and network-level
  errors (timeouts, connection failures) — each surfaced with a clear
  message and non-zero exit code.
- **Testnet only**: base URL defaults to
  `https://testnet.binancefuture.com`; no mainnet endpoint is used or
  supported by default (though `--base-url` can override it if needed).

## Bonus

Not implemented in this submission — happy to add a Stop-Limit / OCO order
type or an interactive CLI menu (e.g. via `questionary`/`rich`) in a
follow-up iteration if useful for evaluation.

## Requirements

See `requirements.txt`:
```
requests>=2.31.0
```
