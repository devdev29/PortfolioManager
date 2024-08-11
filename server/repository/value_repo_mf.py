from datetime import date, timedelta
from dataclasses import astuple

from repository.database_access import get_db_connection
from repository.stock_repo import StockRepo
from repository.mutual_funds_repo import MutualFundsRepo
from repository.account_repo import AccountRepo
from model.value_model import Value

class ValueRepoMF:

    @staticmethod
    def initialise_value(day: date):
        with get_db_connection() as (conn, cursor):
            yesterday = day - timedelta(1)
            stmt = 'select * from value where day=%s'
            cursor.execute(stmt, (day,))
            exists = cursor.fetchone()
            if exists:
                return
            cursor.execute(stmt, (yesterday,))
            yesterday_exists = cursor.fetchone()
            if yesterday_exists:
                stmt = 'insert into value values(%s, %s, %s, %s)'
                yesterday_exists['value'] = float(yesterday_exists['value']) + MutualFundsRepo.get_total_returns()
                yesterday_exists['day'] = day
                yesterday_exists = Value(**yesterday_exists)
                print(yesterday_exists)
                params = astuple(yesterday_exists)
                cursor.execute(stmt, params)
                conn.commit()
                return
            total_value = MutualFundsRepo.get_total_returns() + AccountRepo.get_total_balance()
            value_today = (day, total_value, 0, 0)
            stmt = 'insert into value values(%s, %s, %s, %s)'
            cursor.execute(stmt, value_today)
            conn.commit()
    
    @staticmethod
    def get_value(day: date, dynamic: bool):
        ValueRepoMF.initialise_value(day)
        with get_db_connection() as (_, cursor):
            stmt = 'select * from value where day=%s'
            params = (day,)
            cursor.execute(stmt, params)
            value = cursor.fetchone()
            if dynamic:
                value['value'] = float(value['value']) + MutualFundsRepo.get_total_returns()
            return value
    
    @staticmethod
    def get_history(period: int = 30):
        with get_db_connection() as (_, cursor):
            today = date.today()
            ValueRepoMF.initialise_value(today)
            start_date = today - timedelta(days=period)
            start_value = ValueRepoMF.get_value(start_date)
            if not start_value:
                stmt = "select * from value order by day asc"
                cursor.execute(stmt)
                days = cursor.fetchall()
                start_date = days[0]
            stmt = "select * from value where day >= %s"
            params = (start_date,)
            cursor.execute(stmt, params)
            history = cursor.fetchall()
            return history
    
    @staticmethod
    def update_value_row(value: Value):
        with get_db_connection() as (conn, cursor):
            today = value.day
            ValueRepoMF.initialise_value(today)
            stmt = 'update value set inflow=%s, outflow=%s where day=%s'
            params = (*astuple(value), today)
            params = params[2:]
            cursor.execute(stmt, params)
            conn.commit()
            affected_rows = cursor.rowcount
            return affected_rows
    
    @staticmethod
    def update_inflow(inflow: float):
        today = date.today()
        ValueRepoMF.initialise_value(today)
        value_row = ValueRepoMF.get_value(today, dynamic=False)
        value_row['inflow'] = inflow
        value_row = Value(**value_row)
        res = ValueRepoMF.update_value_row(value_row)
        return res
    
    @staticmethod
    def update_outflow(outflow: float):
        today = date.today()
        ValueRepoMF.initialise_value(today)
        value_row = ValueRepoMF.get_value(today, dynamic=False)
        value_row['outflow'] = outflow
        value_row = Value(**value_row)
        res = ValueRepoMF.update_value_row(value_row)
        return res
    
    @staticmethod
    def update_value(value: float):
        today = date.today()
        ValueRepoMF.initialise_value(today)
        value_row = ValueRepoMF.get_value(today)
        value_row['value'] = value
        res = ValueRepoMF.update_value_row(value_row)
        return res
