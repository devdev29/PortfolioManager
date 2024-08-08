from dataclasses import dataclass
from datetime import date

@dataclass
class Value:
    day: date
    value: float
    inflow: float
    outflow: float
