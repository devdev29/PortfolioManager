import os
import requests
import logging
from datetime import date

from flask import Blueprint, jsonify, request

from model.value_model import Value
from repository.value_repo import ValueRepo

value = Blueprint('value', __name__)

@value.route('/today')
def get_today_value():
    today = date.today()
    value_today = ValueRepo.get_value(today)
    return jsonify(value_today), 200
