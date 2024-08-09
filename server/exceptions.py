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

class MutualFundAlreadyExistsError(Exception):
    def __init__(self, mutual_fund):
        self.mutual_fund = mutual_fund
    def __str__(self) -> str:
        return f'Mutual Fund {self.mutual_fund} already exists in portfolio.'

class MutualFundDoesNotExistError(Exception):
    def __init__(self, mutual_fund):
        self.mutual_fund = mutual_fund
    def __str__(self) -> str:
        return f'Mutual Fund {self.mutual_fund} does not exist in the portfolio.'
    