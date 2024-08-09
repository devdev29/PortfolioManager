import requests
import os

from repository.database_access import get_db_connection
from exceptions import MutualFundAlreadyExistsError, MutualFundDoesNotExistError
from model.mutual_funds_model import MutualFunds
from dataclasses import astuple

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
            stmt = 'select * from mutual funds where mf_id like concat(%s, "%")'
            cursor.execute(stmt, params=(mf_id,))
            mutual_funds = cursor.fetchall()
            return mutual_funds
    
    @staticmethod
    def get_mutual_funds_by_id(mf_id: int):
        with get_db_connection() as (_, cursor):
            stmt = 'select * from mutual_funds where mf_id=%s'
            params = (mf_id,)
            cursor.execute(stmt, params=params)
            mutual_funds = cursor.fetchone()
            return mutual_funds
    
    @staticmethod
    def get_mutual_funds_returns(mf_id: str):
        mutual_funds = MutualFundsRepo.get_mutual_funds_by_id(mf_id)
        if not mutual_funds:
            raise MutualFundDoesNotExistError(mf_id)
        price_res = requests.get(
        f'https://api.mfapi.in/mf/{mf_id}/latest'
        ).json()
        curr_price = float(price_res['data'][0]['nav'])*int(mutual_funds['quantity'])
        mutual_funds_return = float(mutual_funds['amount_invested'])-curr_price
        return mutual_funds_return
    
    @staticmethod
    def get_total_returns():
        total_returns = 0
        mutual_funds = MutualFundsRepo.get_all_mutual_funds()
        for mf in mutual_funds:
            total_returns += MutualFundsRepo.get_mutual_funds_returns(mf['ticker'])
        return total_returns
    
    @staticmethod
    def add_new_mutual_funds(mutual_funds: MutualFunds):
        with get_db_connection() as (conn, cursor):
            exists = MutualFundsRepo.get_mutual_funds_by_id(mutual_funds.mf_id)
            if exists:
                raise MutualFundAlreadyExistsError(mutual_funds.ticker)
            stmt = 'insert into mutual_funds values(%s, %s, %s, %s, %s, %s)'
            params = astuple(mutual_funds)
            cursor.execute(stmt, params=params)
            conn.commit()
            affected_rows = cursor.rowcount
            return affected_rows
    
    @staticmethod
    def update_mutual_funds(mf_id: int, quantity: int, amount_invested: float):
        with get_db_connection() as (conn, cursor):
                stmt = 'update mutual_funds set quantity=%s, amount_invested=%s where mf_id=%s'
                params = (quantity, amount_invested, mf_id)
                cursor.execute(stmt, params=params)
                conn.commit()
                affected_rows = cursor.rowcount
                return affected_rows
    
    @staticmethod
    def remove_mutual_funds(mf_id: int):
        with get_db_connection() as (conn, cursor):
            mutual_funds = MutualFundsRepo.get_mutual_funds_by_id(mf_id)
            if not mutual_funds:
                raise MutualFundDoesNotExistError(mf_id)
            stmt = 'delete from mutual_funds where mf_id=%s'
            params = (mf_id,)
            cursor.execute(stmt, params=params)
            conn.commit()
            affected_rows = cursor.rowcount
            return affected_rows

    
