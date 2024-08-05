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
            stmt = 'select * from stocks where ticker like %s%'
            cursor.execute(stmt, params=(ticker))
            stocks = cursor.fetchall()
            return stocks
    
    @staticmethod
    def get_stock_by_ticker(ticker: str):
        with get_db_connection() as (_, cursor):
            ticker = ticker.upper()
            stmt = 'select * from stocks where ticker=%s'
            params = (ticker)
            cursor.execute(stmt, params=params)
            stock = cursor.fetchone()
            return stock
    
    @staticmethod
    def add_new_stock(stock: Stock):
        with get_db_connection() as (conn, cursor):
            try:
                stmt = 'insert into stocks values(%s, %s, %s, %s, %s, %s, %s)'
                params = stock.to_list()
                cursor.execute(stmt, params=params)
                conn.commit()
                affected_rows = cursor.rowcount
                return affected_rows
            except:
                return -1
    
    @staticmethod
    def update_stock(stock: Stock):
        with get_db_connection() as (conn, cursor):
            try:
                stmt = 'update stocks set values(%s, %s, %s, %s, %s, %s, %s)'
                params = stock.to_list()
                cursor.execute(stmt, params=params)
                conn.commit()
                affected_rows = cursor.rowcount
                return affected_rows
            except:
                return -1
    
    @staticmethod
    def remove_stock(ticker: str):
        with get_db_connection() as (conn, cursor):
            try:
                stmt = 'delete from stocks where ticker=%s'
                params = (ticker)
                cursor.execute(stmt, params=params)
                conn.commit()
                affected_rows = cursor.rowcount
                return affected_rows
            except:
                return -1
    
