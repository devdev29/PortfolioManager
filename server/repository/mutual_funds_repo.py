from repository.database_access import get_db_connection
from model.mutual_funds_model import MutualFunds

class MutualFundsRepo:
    
    @staticmethod
    def get_all_mutual_funds():
        with get_db_connection() as (_, cursor):
            stmt = 'select * from mutual_funds'
            cursor.execute(stmt)
            mutual_funds = cursor.fetchall()
            return mutual_funds
    
    @staticmethod
    def search_mutual_funds_by_id(mf_id: int):
        with get_db_connection() as (_, cursor):
            stmt = 'select * from mutual_funds where mf_id like %d%'
            cursor.execute(stmt, params=(mf_id))
            mutual_funds = cursor.fetchall()
            return mutual_funds
    
    @staticmethod
    def get_mutual_funds_by_id(mf_id: int):
        with get_db_connection() as (_, cursor):
            stmt = 'select * from mutual_funds where mf_id=%d%'
            params = (mf_id)
            cursor.execute(stmt, params=params)
            mutual_funds = cursor.fetchone()
            return mutual_funds
    
    @staticmethod
    def add_new_mutual_funds(mutual_funds: MutualFunds):
        with get_db_connection() as (conn, cursor):
            stmt = 'insert into mutual_funds values(%s, %s, %s, %s, %s)'
            params = mutual_funds.to_list()
            cursor.execute(stmt, params=params)
            conn.commit()
            affected_rows = cursor.rowcount
            return affected_rows
    
    @staticmethod
    def update_mutual_funds(mutual_funds: MutualFunds):
        with get_db_connection() as (conn, cursor):
            stmt = 'update mutual_funds set values(%s, %s, %s, %s, %s)'
            params = mutual_funds.to_list()
            cursor.execute(stmt, params=params)
            conn.commit()
            affected_rows = cursor.rowcount
                

    
    @staticmethod
    def remove_mutual_funds(mf_id: int):
        with get_db_connection() as (conn, cursor):
            stmt = 'delete from mutual_funds where mf_id=%d'
            params = (mf_id)
            cursor.execute(stmt, params=params)
            conn.commit()
            affected_rows = cursor.rowcount
            return affected_rows

    
