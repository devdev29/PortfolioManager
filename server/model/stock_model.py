from dataclasses import dataclass

@dataclass
class Stock:
    ticker: str
    exchange: str
    market_cap: int
    full_name: str
    quantity: int
    amount_invested: float
    account_no: str
    