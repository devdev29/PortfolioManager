import os
import requests
import logging
from datetime import date

from flask import Blueprint, jsonify

from model.account_model import Account
from repository.value_repo import AccountRepo

account = Blueprint('account', __name__)

@account.route('/all', methods=['GET'])
def get_all_accounts():
    try:
        accounts = AccountRepo.get_accounts()
        return jsonify(accounts), 200
    except Exception as e:
        logging.exception(e)
        return jsonify({'message': 'could not get accounts'}), 409

@account.route('/<account_no>', methods=['GET'])
def get_account_by_no(account_no: str):
    try:
        account = AccountRepo.get_account_by_no(account_no)
        return jsonify(account)
    except Exception as e:
        logging.exception(e)
        return jsonify({'message': 'could not get accounts'}), 409

@account.route('/liquidity',  methods=['GET'])
def get_total_liquidity():
    try:
        total_balance = AccountRepo.get_total_balance()
        return jsonify({'balance':total_balance}), 200
    except Exception as e:
        logging.exception(e)
        return jsonify({'message': 'could not get accounts'}), 409

