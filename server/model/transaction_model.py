from dataclasses import dataclass, field
from datetime import date
from uuid import uuid4

@dataclass
class Transaction:
    day: date
    ticker: str
    price: float
    quantity: int
    amount: float
    account_no: str
    transaction_id: str = field(init=False, default_factory=uuid4)
