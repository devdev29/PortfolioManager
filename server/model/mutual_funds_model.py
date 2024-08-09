from dataclasses import dataclass

@dataclass
class MutualFunds:
    name: str
    net_asset_value: float
    mf_id: int
    __quantity: int
    __amount_invested: float
    account_no: str
    
    @property
    def quantity(self):
        return self.__quantity
    
    @property
    def amount_invested(self):
        return self.__amount_invested
    
    @quantity.setter
    def set_quantity(self, new_qty: int):
        self.__quantity = new_qty
        
    @amount_invested.setter
    def set_amount(self, new_price: float):
        self.__amount_invested = new_price
    
    def to_list(self):
        return [
            self.name,
            self.net_asset_value,
            self.mf_id,
            self.__quantity,
            self.__amount_invested,
            self.account_no
        ]
    