import requests
import os
from dataclasses import astuple
from exceptions import StockAlreadyExistsError, StockDoesNotExistError
from repository.database_access import get_db_connection
from model.stock_model import Stock

class StockRepo:
    
    @staticmethod
    def get_all_stocks():
        with get_db_connection() as (_, cursor):
            stmt = 'select * from stocks'
            cursor.execute(stmt)
            stocks = cursor.fetchall()
            return stocks
    
    @staticmethod
    def search_stock_by_ticker(ticker: str):
        with get_db_connection() as (_, cursor):
            ticker = ticker.upper()
            stmt = 'select * from stocks where ticker like concat(%s, "%")'
            cursor.execute(stmt, params=(ticker,))
            stocks = cursor.fetchall()
            return stocks
    
    @staticmethod
    def get_stock_by_ticker(ticker: str):
        with get_db_connection() as (_, cursor):
            ticker = ticker.upper()
            stmt = 'select * from stocks where ticker=%s'
            params = (ticker,)
            cursor.execute(stmt, params=params)
            stock = cursor.fetchone()
            return stock
    
    @staticmethod
    def get_stock_returns(ticker: str):
        ticker = ticker.upper()
        stock = StockRepo.get_stock_by_ticker(ticker)
        if not stock:
            raise StockDoesNotExistError(ticker)
        price_res = requests.get(
        f'https://api.twelvedata.com/price?symbol={ticker}&apikey={os.environ["TWELVE_API_KEY"]}'
        ).json()
        curr_price = float(price_res['price'])*int(stock['quantity'])
        stock_return = float(stock['amount_invested'])-curr_price
        return stock_return

    @staticmethod
    def get_total_returns():
        total_returns = 0
        stocks = StockRepo.get_all_stocks()
        for stock in stocks:
            total_returns += StockRepo.get_stock_returns(stock['ticker'])
        return total_returns

    @staticmethod
    def add_new_stock(stock: Stock):
        with get_db_connection() as (conn, cursor):
                exists = StockRepo.get_stock_by_ticker(stock.ticker)
                if exists:
                    raise StockAlreadyExistsError(stock.ticker)
                stmt = 'insert into stocks values(%s, %s, %s, %s, %s, %s, %s)'
                params = astuple(stock)
                cursor.execute(stmt, params=params)
                conn.commit()
                affected_rows = cursor.rowcount
                return affected_rows
    
    @staticmethod
    def update_stock(ticker: str, quantity: int, amount_invested: float):
        with get_db_connection() as (conn, cursor):
                stmt = 'update stocks set quantity=%s, amount_invested=%s where ticker=%s'
                params = (quantity, amount_invested, ticker)
                cursor.execute(stmt, params=params)
                conn.commit()
                affected_rows = cursor.rowcount
                return affected_rows
    
    @staticmethod
    def remove_stock(ticker: str):
        with get_db_connection() as (conn, cursor):
                stock = StockRepo.get_stock_by_ticker(ticker)
                if not stock:
                    raise StockDoesNotExistError(ticker)
                stmt = 'delete from stocks where ticker=%s'
                params = (ticker,)
                cursor.execute(stmt, params=params)
                conn.commit()
                affected_rows = cursor.rowcount
                return affected_rows
    
