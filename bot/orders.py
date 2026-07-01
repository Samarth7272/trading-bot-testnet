"""Order placement logic: ties validation + client together and formats output."""

import logging

from .client import BinanceAPIError, BinanceFuturesTestnetClient, BinanceNetworkError
from .validators import ValidationError, validate_order_args

logger = logging.getLogger("trading_bot")


class OrderResult:
    """Simple container for a completed (or failed) order attempt."""

    def __init__(self, success: bool, request_summary: dict,
                 response: dict = None, error: str = None):
        self.success = success
        self.request_summary = request_summary
        self.response = response
        self.error = error

    def render(self) -> str:
        """Return a human-readable summary of the order attempt."""
        lines = ["--- Order Request ---"]
        for k, v in self.request_summary.items():
            lines.append(f"  {k}: {v}")

        if self.success:
            lines.append("--- Order Response ---")
            r = self.response or {}
            lines.append(f"  orderId: {r.get('orderId')}")
            lines.append(f"  status: {r.get('status')}")
            lines.append(f"  executedQty: {r.get('executedQty')}")
            avg_price = r.get("avgPrice")
            if avg_price is not None:
                lines.append(f"  avgPrice: {avg_price}")
            lines.append("RESULT: SUCCESS \u2705")
        else:
            lines.append(f"RESULT: FAILURE \u274c ({self.error})")

        return "\n".join(lines)


def place_order(client: BinanceFuturesTestnetClient, symbol: str, side: str,
                 order_type: str, quantity, price=None) -> OrderResult:
    """Validate input and place an order, returning an OrderResult.

    Never raises for expected failure modes (validation, API, network errors);
    those are captured in the returned OrderResult so the CLI can present a
    clean success/failure message.
    """
    try:
        symbol, side, order_type, quantity, price = validate_order_args(
            symbol, side, order_type, quantity, price
        )
    except ValidationError as exc:
        logger.error("Validation failed: %s", exc)
        return OrderResult(
            success=False,
            request_summary={
                "symbol": symbol, "side": side, "type": order_type,
                "quantity": quantity, "price": price,
            },
            error=f"Invalid input: {exc}",
        )

    request_summary = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity,
        "price": price if price is not None else "N/A (market order)",
    }
    logger.info("Placing order: %s", request_summary)

    try:
        response = client.place_order(
            symbol=symbol, side=side, order_type=order_type,
            quantity=quantity, price=price,
        )
    except BinanceAPIError as exc:
        logger.error("Order failed (API error): %s", exc)
        return OrderResult(success=False, request_summary=request_summary,
                            error=f"API error: {exc.message} (code {exc.code})")
    except BinanceNetworkError as exc:
        logger.error("Order failed (network error): %s", exc)
        return OrderResult(success=False, request_summary=request_summary,
                            error=f"Network error: {exc}")

    logger.info("Order placed successfully: orderId=%s status=%s",
                response.get("orderId"), response.get("status"))
    return OrderResult(success=True, request_summary=request_summary, response=response)
