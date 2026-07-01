#!/usr/bin/env python3
"""CLI entry point for the simplified Binance Futures Testnet trading bot.

Examples:
    python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
    python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 60000
"""

import argparse
import os
import sys

from bot.client import BinanceFuturesTestnetClient
from bot.logging_config import setup_logging
from bot.orders import place_order

DEFAULT_BASE_URL = "https://testnet.binancefuture.com"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Place MARKET or LIMIT orders on Binance Futures Testnet (USDT-M).",
    )
    parser.add_argument("--symbol", required=True, help="Trading pair, e.g. BTCUSDT")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL", "buy", "sell"],
                         help="Order side")
    parser.add_argument("--type", dest="order_type", required=True,
                         choices=["MARKET", "LIMIT", "market", "limit"],
                         help="Order type")
    parser.add_argument("--quantity", required=True, help="Order quantity")
    parser.add_argument("--price", required=False, default=None,
                         help="Order price (required for LIMIT orders)")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL,
                         help="Binance Futures Testnet base URL")
    parser.add_argument("-v", "--verbose", action="store_true",
                         help="Enable DEBUG-level logging (full request payloads)")
    return parser


def get_credentials():
    """Load API credentials from environment variables.

    Expects BINANCE_TESTNET_API_KEY and BINANCE_TESTNET_API_SECRET to be set,
    e.g. in a .env file loaded by the shell, or exported directly.
    """
    api_key = os.environ.get("BINANCE_TESTNET_API_KEY")
    api_secret = os.environ.get("BINANCE_TESTNET_API_SECRET")
    if not api_key or not api_secret:
        print(
            "ERROR: Missing API credentials.\n"
            "Set the BINANCE_TESTNET_API_KEY and BINANCE_TESTNET_API_SECRET "
            "environment variables before running.\n"
            "See README.md for setup instructions.",
            file=sys.stderr,
        )
        sys.exit(1)
    return api_key, api_secret


def main():
    parser = build_parser()
    args = parser.parse_args()

    logger = setup_logging(verbose=args.verbose)
    logger.info("=== Trading bot CLI started ===")
    logger.info("Args: symbol=%s side=%s type=%s quantity=%s price=%s",
                args.symbol, args.side, args.order_type, args.quantity, args.price)

    api_key, api_secret = get_credentials()
    client = BinanceFuturesTestnetClient(
        api_key=api_key, api_secret=api_secret, base_url=args.base_url, logger=logger
    )

    result = place_order(
        client=client,
        symbol=args.symbol,
        side=args.side,
        order_type=args.order_type,
        quantity=args.quantity,
        price=args.price,
    )

    print(result.render())
    sys.exit(0 if result.success else 1)


if __name__ == "__main__":
    main()
