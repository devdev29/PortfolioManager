from dataclasses import dataclass

@dataclass
class MutualFunds:
    name: str
    mf_id: int
    net_asset_value: float
    quantity: int
    amount_invested: float
    account_no: str
    
    