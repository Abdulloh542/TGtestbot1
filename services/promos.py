PROMO_CODES = {
    "SALE10": 10,
    "PROMO10": 10,
}


def get_discount_percent(code: str | None) -> int:
    if not code:
        return 0
    return PROMO_CODES.get(code.strip().upper(), 0)
