import os
import requests
import logging
from datetime import date

from flask import Blueprint, jsonify, request

from model.stock_model import Stock
from exceptions import InsufficientFundsError
from repository.stock_repo import StockRepo
from repository.account_repo import AccountRepo
from repository.value_repo import ValueRepo

stocks = Blueprint('stocks', __name__)

STOCK_EXCHANGE = 'BSE'

#Helpers
def update_flows(amount: float, account_no: str):
    AccountRepo.update_amount(account_no, amount)
    #Update total cash flows
    value_row = ValueRepo.get_value(date.today())[0]
    inflow = value_row['inflow']
    outflow = value_row['outflow']
    inflow += amount
    outflow += amount
    ValueRepo.update_inflow(inflow) 
    ValueRepo.update_outflow(outflow)

@stocks.route('/search/<ticker_search>', methods=['GET'])
def get_valid_stocks(ticker_search: str):
    ticker_search = ticker_search.upper()
    res = requests.get(
        f'https://financialmodelingprep.com/api/v3/search?query={ticker_search}&exchange={STOCK_EXCHANGE}&apikey={os.environ["FMP_API_KEY"]}'
        ).json()
    return jsonify(res)

@stocks.route('/portfolio/<ticker_search>', methods=['GET'])
def get_portfolio_stocks(ticker_search: str):
    ticker_search = ticker_search.strip().upper()
    stocks = StockRepo.search_stock_by_ticker(ticker_search)
    return jsonify(stocks), 200

@stocks.route('/portfolio/all', methods=['GET'])
def get_all_stocks():
    stocks = StockRepo.get_all_stocks()
    return jsonify(stocks), 200

@stocks.route('/portfolio', methods=['POST'])
def add_stock():
    # TODO: add logic to calculate and adjust cash flow from given account
    try:
        data = request.json
        ticker = data['ticker']
        price_res = requests.get(
            f'https://api.twelvedata.com/price?symbol={ticker}&exchange={STOCK_EXCHANGE}&apikey={os.environ["TWELVE_API_KEY"]}'
        ).json()
        amount = float(price_res['price'])*float(data['quantity'])
        #Update account state and flows due to stock addition
        update_flows(amount=amount, account_no=data['account_no'])
        data['amount_invested'] = amount
        new_stock = Stock(**data)
        StockRepo.add_new_stock(new_stock)
        return jsonify(new_stock), 201
    except InsufficientFundsError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        logging.exception(e)
        return {'message': 'could not insert stock'}, 409


@stocks.route('/portfolio/<ticker>', methods=['DELETE'])
def delete_stock(ticker: str):
    # TODO: add logic to update liquid balance in account
    try:
        stock = StockRepo.get_stock_by_ticker(ticker)[0]
        price_res = requests.get(
            f'https://api.twelvedata.com/price?symbol={ticker}&exchange={STOCK_EXCHANGE}&apikey={os.environ["TWELVE_API_KEY"]}'
        ).json()
        amount = price_res['price']*stock['quantity']
        update_flows(amount, stock.account_no)
        StockRepo.remove_stock(ticker)
        return jsonify(ticker), 202
    except Exception as e:
        logging.exception(e)
        return jsonify({'message': 'could not remove stock'}), 409

@stocks.route('/portfolio', methods=['PUT'])
def update_stock():
    try:
        data = request.json
        price_res = requests.get(
            f'https://api.twelvedata.com/price?symbol={data['ticker']}&exchange={STOCK_EXCHANGE}&apikey={os.environ["TWELVE_API_KEY"]}'
        ).json()
        amount = price_res['price']*data['quantity']
        data['amount_invested'] = amount
        update_flows(amount, data['account_no'])
        stock = Stock(**data)
        StockRepo.update_stock(stock=stock)
        return jsonify(stock), 204
    except Exception as e:
        logging.exception(e)
        return {'message': 'could not update stock'}, 409

@stocks.route('/performance', methods=['GET'])
def get_stock_performance():
    #TODO: find api that gives stock performance
    ...
