from datetime import date

from repository.database_access import get_db_connection
from model.value_model import Value

class ValueRepo:

    @staticmethod
    def get_value(day: date):
        with get_db_connection() as (_, cursor):
            stmt = 'select * from value where day=%s'
            params = (day)
            cursor.execute(stmt, params=params)
            value = cursor.fetchone()
            return value
    
    @staticmethod
    def update_value_row(value: Value):
        try:
            with get_db_connection() as (conn, cursor):
                today = value['day']
                stmt = 'update value set value(%s, %s, %s) where day=%s'
                params = (*value.to_list(), today)
                cursor.execute(stmt, params=params)
                conn.commit()
                affected_rows = cursor.rowcount
                return affected_rows
        except:
            return -1
    
    @staticmethod
    def update_inflow(inflow: float):
        today = date.today()
        value_row = ValueRepo.get_value(today)
        value_row['inflow'] = inflow
        res = ValueRepo.update_value_row(value_row)
        return res
    
    @staticmethod
    def update_outflow(outflow: float):
        today = date.today()
        value_row = ValueRepo.get_value(today)
        value_row['outflow'] = outflow
        res = ValueRepo.update_value_row(value_row)
        return res
    
    @staticmethod
    def update_value(value: float):
        today = date.today()
        value_row = ValueRepo.get_value(today)
        value_row['value'] = value
        res = ValueRepo.update_value_row(value_row)
        return res
