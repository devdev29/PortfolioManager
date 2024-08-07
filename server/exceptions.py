class InsufficientFundsError(ValueError):
    def __init__(self, amount):
        self.amount = amount
    def __str__(self):
        return f'Insufficient amount {self.amount} to buy asset'

class StockAlreadyExistsError(Exception):
    def __init__(self, stock) -> None:
        self.stock = stock
    def __str__(self) -> str:
        return f'Stock {self.stock} already exists in portfolio'
    