import os
import requests

from flask import Blueprint, jsonify, request

from model.mutual_funds_model import MutualFunds
from repository.mutual_funds_repo import MutualFundsRepo

mutual_funds = Blueprint('mutual_funds', __name__)


@mutual_funds.route('/mutual_funds/search/', methods=['GET'])
def get_valid_mutual_funds():
    res = requests.get(
        f'https://api.mfapi.in/mf'
        )
    #print(type(res.text))
    return res.text

# @mutual_funds.route('/mutual_funds/search/<mutual_funds_id>', methods=['GET'])
# def get_valid_mutual_funds(mf_id: int):
#     mutual_funds = MutualFundsRepo.search_mutual_funds_by_id(mf_id)
#     mf_id = 
#     res = requests.get(
#         f'https://api.mfapi.in/mf/{mf_id}/latest'
#         )
#     return jsonify(mutual_funds), 200

@mutual_funds.route('/mutual_funds/portfolio/<mutual_funds_id>', methods=['GET'])
def get_portfolio_mutual_funds(mutual_funds_id: int):
    mutual_funds = MutualFundsRepo.search_mutual_funds_by_id(mutual_funds_id)
    return jsonify(mutual_funds), 200

@mutual_funds.route('/mutual_funds/portfolio', methods=['POST'])
def add_mutual_funds():
    # TODO: add logic to calculate and adjust cash flow from given account
    data = request.json
    mf_id = data['mf_id']
    price_res = requests.get(
        f'https://api.mfapi.in/mf/{mf_id}/latest'
    ).json()
    print(price_res['data'][0]['nav'])
    amount = price_res['data'][0]['nav']*data['quantity']
    data['amount_invested'] = amount
    new_mf = MutualFunds(**data)       
    added = MutualFundsRepo.add_new_mutual_fund(new_mf)
    if added == 1:
        return jsonify(new_mf), 200
    return {'message': 'could not insert stock'}, 400


@mutual_funds.route('/mutual_funds/portfolio/<mf_id>', methods=['DELETE'])
def delete_mutual_funds(mf_id: int):
    # TODO: add logic to update liquid balance in account
    res = MutualFundsRepo.remove_stock(mf_id)
    if res == 1:
        return jsonify(mf_id), 200
    return {'message': 'could not remove stock'}, 500

@mutual_funds.route('/mutual_funds/portfolio', methods=['PUT'])
def update_mutual_funds():
    data = request.json
    mf_id = data['mf_id']
    price_res = requests.get(
        f'https://api.mfapi.in/mf/{mf_id}/latest'
    ).json()
    amount = price_res['data'][0]['nav']*data['quantity']
    data['amount_invested'] = amount
    mutual_funds = MutualFunds(**data)
    res = MutualFundsRepo.update_mutual_funds(mutual_funds=mutual_funds)
    if res == 1:
        return jsonify(res), 200
    return {'message': 'could not update stock'}, 500