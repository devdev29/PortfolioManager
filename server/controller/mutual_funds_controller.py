import os
import requests
import logging
from datetime import date

from flask import Blueprint, jsonify, request

from model.mutual_funds_model import MutualFunds
from model.transaction_model import Transaction
from repository.mutual_funds_repo import MutualFundsRepo
from repository.account_repo import AccountRepo
from repository.value_repo_mf import ValueRepoMF
from repository.transaction_repo import TransactionRepo
from exceptions import InsufficientFundsError, MutualFundDoesNotExistError

mutual_funds = Blueprint('mutual_funds', __name__)

#Helpers
def update_flows(amount: float, account_no: str, price: float, quantity: int, mf_id: str):
    AccountRepo.update_amount(account_no, amount)
    #Update total cash flows
    value_row = ValueRepoMF.get_value(date.today(), dynamic=False)
    if amount > 0:
        # selling should increase inflow
        inflow = value_row['inflow']
        inflow += amount
        ValueRepoMF.update_inflow(inflow)
    else:
        # buying should increase outflow
        outflow = value_row['outflow']
        outflow += amount 
        ValueRepoMF.update_outflow(outflow)
    transaction = Transaction(
        day=date.today(), price=price, quantity=quantity, amount=amount, account_no=account_no, ticker=mf_id
    )
    TransactionRepo.add_transaction(transaction)
    

# @mutual_funds.route('/search/', methods=['GET'])
# def get_valid_mutual_funds():
#     res = requests.get(
#         f'https://api.mfapi.in/mf'
#         )
#     #print(type(res.text))
#     return jsonify(res)

@mutual_funds.route('/search/<mf_id>', methods=['GET'])
def get_valid_mutual_funds(mf_id: int):
    try:
        res = requests.get(
            f'https://api.mfapi.in/mf/{mf_id}/latest'
            ).json()
        return jsonify(res), 200
    except Exception as e:
        logging.exception(e)
        return jsonify({'message', 'could not get mutual funds'}), 409

@mutual_funds.route('/portfolio/<mf_id>', methods=['GET'])
def get_portfolio_mutual_funds(mf_id: int):
    try:
        
        mutual_funds = MutualFundsRepo.search_mutual_funds_by_id(mf_id)
        return jsonify(mutual_funds), 200
    except Exception as e:
        logging.exception(e)
        return jsonify({'message', 'could not get mutual funds'}), 409
        

@mutual_funds.route('/portfolio/all', methods=['GET'])
def get_all_mutual_funds():
    try:
        mutual_funds = MutualFundsRepo.get_all_mutual_funds()
        return jsonify(mutual_funds), 200
    except Exception as e:
        logging.exception(e)
        return jsonify({'message', 'could not get mutual fund'}), 409

@mutual_funds.route('/portfolio', methods=['POST'])
def add_mutual_funds():
    try:
        data = request.json
        mf_id = data['mf_id']
        price_res = requests.get(
        f'https://api.mfapi.in/mf/{mf_id}/latest'
        ).json()
        amount = float(price_res['data'][0]['nav'])*int(data['quantity'])
        #Update account state and flows due to mutual fund addition
        update_flows(-amount, data['account_no'], price_res['data'][0]['nav'], int(data['quantity']), mf_id)
        data['amount_invested'] = amount
        new_mf = MutualFunds(**data)
        MutualFundsRepo.add_new_mutual_funds(new_mf)
        return jsonify(new_mf), 201
    except InsufficientFundsError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        logging.exception(e)
        return {'message': 'could not insert mutual fund'}, 409


@mutual_funds.route('/portfolio/<mf_id>', methods=['DELETE'])
def delete_mutual_funds(mf_id: int):
    # TODO: add logic to update liquid balance in account
    try:
        mutual_funds = MutualFundsRepo.get_mutual_funds_by_id(mf_id)
        price_res = requests.get(
            f'https://api.mfapi.in/mf/{mf_id}/latest'
        ).json()
        MutualFundsRepo.remove_mutual_funds(mf_id)
        amount = float(price_res['data'][0]['nav'])*int(mutual_funds['quantity'])
        update_flows(amount, mutual_funds['account_no'], price_res['data'][0]['nav'], int(mutual_funds['quantity']), mf_id)
        return jsonify(mf_id), 202
    except MutualFundDoesNotExistError as e:
        return jsonify({'message': str(e)})
    except Exception as e:
        logging.exception(e)
        return jsonify({'message': 'could not remove mutual fund'}), 409

@mutual_funds.route('/portfolio', methods=['PUT'])
def update_mutual_funds():
    try:
        data = request.json
        mf_id = data['mf_id']
        mutual_funds = MutualFundsRepo.get_mutual_funds_by_id(data['mf_id'])
        price_res = requests.get(
            f'https://api.mfapi.in/mf/{mf_id}/latest'
        ).json()
        amount = float(price_res['data'][0]['nav'])*int(data['quantity'])
        data['amount_invested'] = amount
        flow = float(mutual_funds['amount_invested'])-amount
        MutualFundsRepo.update_mutual_funds(data['mf_id'], quantity=data['quantity'], amount_invested=amount)
        update_flows(flow, mutual_funds['account_no'], price_res['data'][0]['nav'], int(data['quantity']), mf_id)
        return jsonify(mutual_funds), 204
    except Exception as e:
        logging.exception(e)
        return {'message': 'could not update mutual fund'}, 409

@mutual_funds.route('/portfolio/returns', methods=['GET'])
def get_total_returns():
    try:
        total_returns = MutualFundsRepo.get_total_returns()
        return {'returns': total_returns}, 200
    except Exception as e:
        logging.exception(e)
        return jsonify({'message', 'could not get mutual funds'}), 409
        

@mutual_funds.route('/portfolio/returns/<mf_id>', methods=['GET'])
def get_returns(mf_id: int):
    try:
        mutual_funds_returns = MutualFundsRepo.get_mutual_funds_returns(mf_id)
        return jsonify({'returns':mutual_funds_returns}), 200
    except MutualFundDoesNotExistError as e:
        return jsonify({'message':str(e)}), 400
    except Exception as e:
        logging.exception(e)
        return jsonify({'message':'Could not get returns'}), 409

@mutual_funds.route('/portfolio/performance', methods=['GET'])
def get_mutual_funds_performance():
    #TODO: find api that gives mutual_funds performance
    try:
        performance={'gainers':[], 'losers':[]}
        all_mutual_funds = MutualFundsRepo.get_all_mutual_funds()
        for mutual_funds in all_mutual_funds:
            mf_id = mutual_funds['mf_id']
            mutual_funds_quote = requests.get(
                f'https://api.mfapi.in/mf/{mf_id}/latest'
            ).json()
            float_percent = float(mutual_funds_quote['percent_change'])
            if float_percent > 0:
                performance['gainers'].append({mf_id: float_percent})
            else:
                performance['losers'].append({mf_id: float_percent})
            
        performance['gainers'] = sorted(performance['gainers'], key = lambda gainer: float(list(gainer.values())[0]))
        performance['losers'] = sorted(performance['losers'], key = lambda loser: float(list(loser.values())[0]), reverse=True)
        return performance, 200
    except Exception as e:
        logging.exception(e)
        return jsonify({'message', 'could not get mutual funds'}), 409
