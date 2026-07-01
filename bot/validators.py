"""Input validation helpers for CLI order arguments."""

import re

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}
SYMBOL_PATTERN = re.compile(r"^[A-Z0-9]{5,20}$")


class ValidationError(ValueError):
    """Raised when user-supplied order input fails validation."""


def validate_symbol(symbol: str) -> str:
    """Validate and normalize a trading pair symbol, e.g. 'btcusdt' -> 'BTCUSDT'."""
    if not symbol:
        raise ValidationError("Symbol is required.")
    symbol = symbol.strip().upper()
    if not SYMBOL_PATTERN.match(symbol):
        raise ValidationError(
            f"Invalid symbol '{symbol}'. Expected a format like 'BTCUSDT'."
        )
    return symbol


def validate_side(side: str) -> str:
    """Validate order side is BUY or SELL."""
    if not side:
        raise ValidationError("Side is required.")
    side = side.strip().upper()
    if side not in VALID_SIDES:
        raise ValidationError(f"Invalid side '{side}'. Must be one of {VALID_SIDES}.")
    return side


def validate_order_type(order_type: str) -> str:
    """Validate order type is MARKET or LIMIT."""
    if not order_type:
        raise ValidationError("Order type is required.")
    order_type = order_type.strip().upper()
    if order_type not in VALID_ORDER_TYPES:
        raise ValidationError(
            f"Invalid order type '{order_type}'. Must be one of {VALID_ORDER_TYPES}."
        )
    return order_type


def validate_quantity(quantity) -> float:
    """Validate quantity is a positive number."""
    try:
        quantity = float(quantity)
    except (TypeError, ValueError):
        raise ValidationError(f"Quantity must be a number, got '{quantity}'.")
    if quantity <= 0:
        raise ValidationError("Quantity must be greater than 0.")
    return quantity


def validate_price(price, order_type: str):
    """Validate price: required and positive for LIMIT orders, ignored for MARKET."""
    if order_type == "MARKET":
        return None
    if price is None:
        raise ValidationError("Price is required for LIMIT orders.")
    try:
        price = float(price)
    except (TypeError, ValueError):
        raise ValidationError(f"Price must be a number, got '{price}'.")
    if price <= 0:
        raise ValidationError("Price must be greater than 0.")
    return price


def validate_order_args(symbol: str, side: str, order_type: str, quantity, price=None):
    """Validate a full set of order arguments and return normalized values.

    Returns:
        tuple: (symbol, side, order_type, quantity, price)
    """
    symbol = validate_symbol(symbol)
    side = validate_side(side)
    order_type = validate_order_type(order_type)
    quantity = validate_quantity(quantity)
    price = validate_price(price, order_type)
    return symbol, side, order_type, quantity, price
