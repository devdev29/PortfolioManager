import os
import requests
import logging
from datetime import date

from flask import Blueprint, jsonify, request

from model.value_model import Value
from repository.value_repo import ValueRepo
from exceptions import InsufficientAPICredits

value = Blueprint('value', __name__)

@value.route('/today')
def get_today_value():
    try:
        today = date.today()
        value_today = ValueRepo.get_value(today, dynamic=False)
        return jsonify(value_today), 200
    except InsufficientAPICredits as e:
        return jsonify({'message':str(e)}), 403
    except Exception as e:
        logging.exception(e)
        return jsonify({'message':'could not get value'}), 409

@value.route('/history')
@value.route('/history/<period>')
def get_history(period: int = 30):
    try:
        history = ValueRepo.get_history(period)
        return jsonify(history), 200
    except Exception as e:
        logging.exception(e)
        return jsonify({'message':'could not get history'})
