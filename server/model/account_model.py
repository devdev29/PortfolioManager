from dataclasses import dataclass

@dataclass
class Account:
    account_no: str
    bank_name: str
    account_type: str
    amount: float
    
