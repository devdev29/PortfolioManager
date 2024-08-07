from dataclasses import dataclass

@dataclass
class Stock:
    ticker: str
    exchange: str
    market_cap: int
    full_name: str
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
            self.ticker,
            self.exchange,
            self.market_cap,
            self.full_name,
            self.__quantity,
            self.__amount_invested,
            self.account_no
        ]
    