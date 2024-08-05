from repository.database_access import get_db_connection
from model.account_model import Account

class AccountRepo:

    @staticmethod
    def get_accounts():
        with get_db_connection() as (_, cursor):
            stmt = 'select * from accounts'
            cursor.execute(stmt)
            accounts = cursor.fetchall()
            return accounts
    
    @staticmethod
    def get_account_by_no(account_no: str):
        with get_db_connection() as (_, cursor):
            stmt = 'select * from accounts where account_no=%s'
            params = (account_no)
            cursor.execute(stmt, params=params)
            account = cursor.fetchone()
            return account
    
    @staticmethod
    def add_account(account: Account):
        with get_db_connection() as (conn, cursor):
            try:
                stmt = 'insert into accounts values(%s, %s, %s, %s)'
                params = account.to_list()
                cursor.execute(stmt, params=params)
                conn.commit()
                affected_rows = cursor.rowcount
                return affected_rows
            except:
                return -1
    
    @staticmethod
    def remove_account(account_no: str):
        with get_db_connection() as (conn, cursor):
            try:
                stmt = 'delete from accounts where account_no=%s'
                params = (account_no)
                cursor.execute(stmt, params=params)
                conn.commit()
                affected_rows = cursor.rowcount
                return affected_rows
            except:
                return -1
    
    @staticmethod
    def update_account(account: Account):
        with get_db_connection() as (conn, cursor):
            try:
                account_no = account.account_no
                stmt = 'update accounts set values(%s, %s, %s, %s) where account_no=%s'
                params = account.to_list().append(account_no)
                cursor.execute(stmt, params=params)
                conn.commit()
                affected_rows = cursor.rowcount
                return affected_rows
            except:
                 return -1
    
    @staticmethod
    def update_amount(account_no: str, amount: float):
        try:
            account = AccountRepo.get_account_by_no(account_no)
            account = account[0]
            account.amount = amount
            affected_rows = AccountRepo.update_account(account)
            return affected_rows
        except:
            return -1
