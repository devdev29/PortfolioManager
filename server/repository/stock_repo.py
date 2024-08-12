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
            ticker = f'{ticker}%'
            stmt = 'select * from stocks where ticker like %s'
            cursor.execute(stmt, (ticker,))
            stocks = cursor.fetchall()
            return stocks
    
    @staticmethod
    def get_stock_by_ticker(ticker: str):
        with get_db_connection() as (_, cursor):
            ticker = ticker.upper()
            stmt = 'select * from stocks where ticker=%s'
            params = (ticker,)
            cursor.execute(stmt, params)
            stock = cursor.fetchone()
            return stock
    
    @staticmethod
    def get_stock_returns(ticker: str):
        ticker = ticker.upper()
        stock = StockRepo.get_stock_by_ticker(ticker)
        if not stock:
            raise StockDoesNotExistError(ticker)
        price_res = requests.get(
        f'https://financialmodelingprep.com/api/v3/quote-short/{ticker}?apikey={os.environ["FMP_API_KEY"]}'
        ).json()[0]
        curr_price = float(price_res['price'])*int(stock['quantity'])
        stock_return = curr_price-float(stock['amount_invested'])
        return stock_return

    @staticmethod
    def get_total_returns():
        total_returns = 0
        stocks = StockRepo.get_all_stocks()
        tickers = ''
        for stock in stocks:
            tickers += f'{stock['ticker']},'
        price_res = requests.get(
        f'https://financialmodelingprep.com/api/v3/quote-short/{tickers}?apikey={os.environ["FMP_API_KEY"]}'
        ).json()
        for price in price_res:
            ticker = price['symbol']
            stock = StockRepo.get_stock_by_ticker(ticker)
            curr_price = float(price['price'])*int(stock['quantity'])
            stock_return = curr_price-float(stock['amount_invested'])
            total_returns+=stock_return
        return total_returns

    @staticmethod
    def add_new_stock(stock: Stock):
        with get_db_connection() as (conn, cursor):
                exists = StockRepo.get_stock_by_ticker(stock.ticker)
                if exists:
                    raise StockAlreadyExistsError(stock.ticker)
                stmt = 'insert into stocks values(%s, %s, %s, %s, %s, %s, %s)'
                params = astuple(stock)
                cursor.execute(stmt, params)
                conn.commit()
                affected_rows = cursor.rowcount
                return affected_rows
    
    @staticmethod
    def update_stock(ticker: str, quantity: int, amount_invested: float):
        with get_db_connection() as (conn, cursor):
                stmt = 'update stocks set quantity=%s, amount_invested=%s where ticker=%s'
                params = (quantity, amount_invested, ticker)
                cursor.execute(stmt, params)
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
                cursor.execute(stmt, params)
                conn.commit()
                affected_rows = cursor.rowcount
                return affected_rows
    
