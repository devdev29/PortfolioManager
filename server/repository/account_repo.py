from dataclasses import astuple
from repository.database_access import get_db_connection
from model.account_model import Account
from exceptions import InsufficientFundsError, AccountDoesNotExistError

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
            params = (account_no,)
            cursor.execute(stmt, params=params)
            account = cursor.fetchone()
            return account
    
    @staticmethod
    def add_account(account: Account):
        with get_db_connection() as (conn, cursor):
                stmt = 'insert into accounts values(%s, %s, %s, %s)'
                params = astuple(account)
                cursor.execute(stmt, params=params)
                conn.commit()
                affected_rows = cursor.rowcount
                return affected_rows
    
    @staticmethod
    def remove_account(account_no: str):
        with get_db_connection() as (conn, cursor):
                stmt = 'delete from accounts where account_no=%s'
                params = (account_no,)
                cursor.execute(stmt, params=params)
                conn.commit()
                affected_rows = cursor.rowcount
                return affected_rows
    
    @staticmethod
    def update_amount(account_no: str, diff: float):
        with get_db_connection() as (conn, cursor):
            account = AccountRepo.get_account_by_no(account_no)
            if not account:
                AccountDoesNotExistError(account_no)
            new_amount = account['amount'] + diff
            if new_amount < 0:
                raise InsufficientFundsError(account['amount'])
            stmt = 'update accounts set amount=%s where account_no=%s'
            params = (new_amount, account_no)
            cursor.execute(stmt, params=params)
            conn.commit()
            return new_amount
    
    @staticmethod
    def get_total_balance():
        balance = 0
        accounts = AccountRepo.get_accounts()
        for account in accounts:
            balance += float(account['amount'])
        return balance
