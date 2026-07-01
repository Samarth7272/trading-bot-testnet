"""Thin wrapper around the Binance Futures Testnet (USDT-M) REST API.

Implemented with direct REST calls (requests) rather than python-binance so
the request/response cycle is fully transparent for logging purposes and to
avoid a hard dependency on a third-party SDK's testnet support.

Docs: https://binance-docs.github.io/apidocs/testnet/en/
"""

import hashlib
import hmac
import logging
import time
from urllib.parse import urlencode

import requests

DEFAULT_BASE_URL = "https://testnet.binancefuture.com"
RECV_WINDOW_MS = 5000
REQUEST_TIMEOUT_S = 10


class BinanceAPIError(Exception):
    """Raised when the Binance API returns an error response."""

    def __init__(self, status_code, code, message):
        self.status_code = status_code
        self.code = code
        self.message = message
        super().__init__(f"Binance API error {code} (HTTP {status_code}): {message}")


class BinanceNetworkError(Exception):
    """Raised when the request to Binance fails at the network level."""


class BinanceFuturesTestnetClient:
    """Minimal signed REST client for Binance USDT-M Futures Testnet."""

    def __init__(self, api_key: str, api_secret: str, base_url: str = DEFAULT_BASE_URL,
                 logger: logging.Logger = None):
        if not api_key or not api_secret:
            raise ValueError("api_key and api_secret are required.")
        self.api_key = api_key
        self.api_secret = api_secret.encode("utf-8")
        self.base_url = base_url.rstrip("/")
        self.logger = logger or logging.getLogger("trading_bot")
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": self.api_key})

    # -- internal helpers ---------------------------------------------------

    def _sign(self, params: dict) -> dict:
        params = dict(params)
        params["timestamp"] = int(time.time() * 1000)
        params.setdefault("recvWindow", RECV_WINDOW_MS)
        query_string = urlencode(params, doseq=True)
        signature = hmac.new(self.api_secret, query_string.encode("utf-8"), hashlib.sha256).hexdigest()
        params["signature"] = signature
        return params

    def _request(self, method: str, path: str, params: dict = None, signed: bool = False):
        url = f"{self.base_url}{path}"
        params = params or {}
        if signed:
            params = self._sign(params)

        # Log the outgoing request (mask the signature to keep logs clean).
        safe_params = {k: v for k, v in params.items() if k != "signature"}
        self.logger.info("REQUEST %s %s params=%s", method, path, safe_params)
        self.logger.debug("Full request params (incl. signature): %s", params)

        try:
            response = self.session.request(
                method, url, params=params, timeout=REQUEST_TIMEOUT_S
            )
        except requests.exceptions.RequestException as exc:
            self.logger.error("NETWORK ERROR on %s %s: %s", method, path, exc)
            raise BinanceNetworkError(str(exc)) from exc

        self.logger.info("RESPONSE %s %s status=%s body=%s",
                          method, path, response.status_code, response.text)

        try:
            data = response.json()
        except ValueError:
            data = {"raw": response.text}

        if response.status_code >= 400:
            code = data.get("code", response.status_code)
            message = data.get("msg", response.text)
            self.logger.error("API ERROR %s %s: code=%s msg=%s", method, path, code, message)
            raise BinanceAPIError(response.status_code, code, message)

        return data

    # -- public API -----------------------------------------------------

    def ping(self):
        """Test connectivity to the testnet REST API."""
        return self._request("GET", "/fapi/v1/ping")

    def get_server_time(self):
        """Get testnet server time."""
        return self._request("GET", "/fapi/v1/time")

    def place_order(self, symbol: str, side: str, order_type: str,
                     quantity: float, price: float = None,
                     time_in_force: str = "GTC"):
        """Place a MARKET or LIMIT order on Binance Futures Testnet.

        Args:
            symbol: trading pair, e.g. 'BTCUSDT'
            side: 'BUY' or 'SELL'
            order_type: 'MARKET' or 'LIMIT'
            quantity: order quantity
            price: required for LIMIT orders
            time_in_force: required for LIMIT orders (default 'GTC')

        Returns:
            dict: parsed JSON order response from Binance.
        """
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }
        if order_type == "LIMIT":
            if price is None:
                raise ValueError("price is required for LIMIT orders.")
            params["price"] = price
            params["timeInForce"] = time_in_force

        return self._request("POST", "/fapi/v1/order", params=params, signed=True)

    def get_order(self, symbol: str, order_id: int):
        """Query an order's status by orderId."""
        params = {"symbol": symbol, "orderId": order_id}
        return self._request("GET", "/fapi/v1/order", params=params, signed=True)
