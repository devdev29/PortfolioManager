class InsufficientFundsError(ValueError):
    def __init__(self, amount):
        self.amount = amount
    def __str__(self) -> str:
        return f'Insufficient amount {self.amount} to buy asset.'

class StockAlreadyExistsError(Exception):
    def __init__(self, stock):
        self.stock = stock
    def __str__(self) -> str:
        return f'Stock {self.stock} already exists in portfolio.'

class StockDoesNotExistError(Exception):
    def __init__(self, stock):
        self.stock = stock
    def __str__(self) -> str:
        return f'Stock {self.stock} does not exist in the portfolio.'
    