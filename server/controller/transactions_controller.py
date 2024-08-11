import logging
from datetime import date

from flask import Blueprint, jsonify

from repository.transaction_repo import TransactionRepo

transactions = Blueprint('transactions', __name__)

@transactions.route('/history')
@transactions.route('history/<date>')
def get_transactions(date: date = date.today()):
    try:
        transactions = TransactionRepo.get_transactions(date)
        return jsonify(transactions), 200
    except Exception as e:
        logging.exception(e)
        return jsonify({'message':'could not fetch transactions!'})
