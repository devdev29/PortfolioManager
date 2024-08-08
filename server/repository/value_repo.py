from datetime import date, timedelta

from repository.database_access import get_db_connection
from repository.stock_repo import StockRepo
from repository.account_repo import AccountRepo
from model.value_model import Value

class ValueRepo:

    @staticmethod
    def initialise_value(day: date):
        with get_db_connection() as (conn, cursor):
            yesterday = day - timedelta(1)
            stmt = 'select * from value where day=%s'
            cursor.execute(stmt, params=(day,))
            exists = cursor.fetchone()
            if exists:
                return
            cursor.execute(stmt, params=(yesterday,))
            yesterday_exists = cursor.fetchone()
            if yesterday_exists:
                stmt = 'update value set values(%s, %s, %s)'
                params = yesterday_exists[0].to_list()
                cursor.execute(stmt, params=params)
                conn.commit()
                return
            total_value = StockRepo.get_total_returns() + AccountRepo.get_total_balance()
            value_today = (total_value, 0, 0)
            stmt = 'insert into value values(%s, %s, %s)'
            cursor.execute(stmt, params=value_today)
            conn.commit()
    
    @staticmethod
    def get_value(day: date):
        ValueRepo.initialise_value(day)
        with get_db_connection() as (_, cursor):
            stmt = 'select * from value where day=%s'
            params = (day)
            cursor.execute(stmt, params=params)
            value = cursor.fetchone()
            value = float(value[0]['value']) + StockRepo.get_total_returns()
            return value
    
    @staticmethod
    def get_history(period: int = 30):
        with get_db_connection() as (_, cursor):
            today = date.today()
            ValueRepo.initialise_value(today)
            start_date = today - timedelta(days=period)
            start_value = ValueRepo.get_value(start_date)
            if not start_value:
                stmt = "select * from value order by day asc"
                cursor.execute(stmt)
                days = cursor.fetchall()
                start_date = days[0]
            stmt = "select * from value where day >= %s"
            params = (start_date,)
            cursor.execute(stmt, params=params)
            history = cursor.fetchall()
            return history
    
    @staticmethod
    def update_value_row(value: Value):
        with get_db_connection() as (conn, cursor):
            today = value['day']
            ValueRepo.initialise_value(today)
            stmt = 'update value set value(%s, %s, %s) where day=%s'
            params = (*value.to_list(), today)
            cursor.execute(stmt, params=params)
            conn.commit()
            affected_rows = cursor.rowcount
            return affected_rows
    
    @staticmethod
    def update_inflow(inflow: float):
        today = date.today()
        ValueRepo.initialise_value(today)
        value_row = ValueRepo.get_value(today)
        value_row['inflow'] = inflow
        res = ValueRepo.update_value_row(value_row)
        return res
    
    @staticmethod
    def update_outflow(outflow: float):
        today = date.today()
        ValueRepo.initialise_value(today)
        value_row = ValueRepo.get_value(today)
        value_row['outflow'] = outflow
        res = ValueRepo.update_value_row(value_row)
        return res
    
    @staticmethod
    def update_value(value: float):
        today = date.today()
        ValueRepo.initialise_value(today)
        value_row = ValueRepo.get_value(today)
        value_row['value'] = value
        res = ValueRepo.update_value_row(value_row)
        return res
