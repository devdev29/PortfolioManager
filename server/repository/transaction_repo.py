from dataclasses import astuple
from datetime import date

from repository.database_access import get_db_connection
from model.transaction_model import Transaction

class TransactionRepo:
    
    @staticmethod
    def add_transaction(transaction: Transaction):
        with get_db_connection() as (conn, cursor):
            stmt = 'insert into transactions values(%s, %s, %s, %s, %s, %s, %s)'
            params = astuple(transaction)
            cursor.execute(stmt, params)
            conn.commit()
            affected_rows = cursor.rowcount
            return affected_rows
    
    @staticmethod
    def get_transactions(day = date.today()):
        with get_db_connection() as (_, cursor):
            stmt = 'select * from transactions where day=%s'
            params = (day,)
            cursor.execute(stmt, params)
            transactions = cursor.fetchall()
            return transactions
