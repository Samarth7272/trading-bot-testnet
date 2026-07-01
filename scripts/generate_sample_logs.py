"""Generates sample log entries for one MARKET and one LIMIT order by mocking
the Binance Futures Testnet HTTP layer. This is only used to produce the
required sample log files for the assignment deliverable -- it does not hit
the real testnet and requires no credentials.

Run with: python scripts/generate_sample_logs.py
"""

import json
import sys
import time
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from bot.client import BinanceFuturesTestnetClient
from bot.logging_config import setup_logging
from bot.orders import place_order


def make_mock_response(order_id, symbol, side, order_type, quantity, price, status):
    resp = MagicMock()
    resp.status_code = 200
    body = {
        "orderId": order_id,
        "symbol": symbol,
        "status": status,
        "side": side,
        "type": order_type,
        "executedQty": quantity if order_type == "MARKET" else "0",
        "origQty": quantity,
        "avgPrice": price if order_type == "MARKET" else "0.00",
        "price": price or "0",
        "updateTime": int(time.time() * 1000),
    }
    resp.text = json.dumps(body)
    resp.json.return_value = body
    return resp


def main():
    logger = setup_logging(verbose=True)
    client = BinanceFuturesTestnetClient(
        api_key="sample_api_key_for_demo",
        api_secret="sample_api_secret_for_demo",
        logger=logger,
    )

    with patch.object(client.session, "request") as mock_request:
        # 1. MARKET order
        mock_request.return_value = make_mock_response(
            order_id=100001, symbol="BTCUSDT", side="BUY", order_type="MARKET",
            quantity="0.01", price="60123.50", status="FILLED",
        )
        result = place_order(client, symbol="BTCUSDT", side="BUY",
                              order_type="MARKET", quantity="0.01")
        print(result.render())
        print()

        # 2. LIMIT order
        mock_request.return_value = make_mock_response(
            order_id=100002, symbol="ETHUSDT", side="SELL", order_type="LIMIT",
            quantity="0.5", price="3200.00", status="NEW",
        )
        result = place_order(client, symbol="ETHUSDT", side="SELL",
                              order_type="LIMIT", quantity="0.5", price="3200.00")
        print(result.render())

    print("\nSample logs written to logs/trading_bot.log")


if __name__ == "__main__":
    main()
