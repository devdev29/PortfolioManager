import os
import requests
import logging
from datetime import date

from flask import Blueprint, jsonify, request

from model.stock_model import Stock
from model.transaction_model import Transaction
from exceptions import InsufficientFundsError, StockDoesNotExistError, StockAlreadyExistsError
from repository.stock_repo import StockRepo
from repository.account_repo import AccountRepo
from repository.value_repo import ValueRepo
from repository.transaction_repo import TransactionRepo

stocks = Blueprint('stocks', __name__)

STOCK_EXCHANGE = 'nasdaq'

#Helpers
def update_flows(amount: float, account_no: str, quantity: int, price: float, ticker: str):
    AccountRepo.update_amount(account_no, amount)
    #Update total cash flows
    value_row = ValueRepo.get_value(date.today(), dynamic=False)
    if amount > 0:
        # selling should increase inflow
        inflow = value_row['inflow']
        inflow += amount
        ValueRepo.update_inflow(inflow)
    else:
        # buying should increase outflow
        outflow = value_row['outflow']
        outflow += amount 
        ValueRepo.update_outflow(outflow)
    # Register the transaction
    transaction = Transaction(
        day=date.today(), price=price, quantity=quantity, amount=amount, account_no=account_no, ticker=ticker
    )
    TransactionRepo.add_transaction(transaction)

@stocks.route('/search/<ticker_search>', methods=['GET'])
def get_valid_stocks(ticker_search: str):
    try:
        ticker_search = ticker_search.upper()
        res = requests.get(
            f'https://financialmodelingprep.com/api/v3/search?query={ticker_search}&exchange={STOCK_EXCHANGE}&apikey={os.environ["FMP_API_KEY"]}'
            ).json()
        return jsonify(res)
    except Exception as e:
        logging.exception(e)
        return jsonify({'message', 'could not get stocks'}), 409

@stocks.route('/portfolio/<ticker_search>', methods=['GET'])
def get_portfolio_stocks(ticker_search: str):
    try:
        ticker_search = ticker_search.strip().upper()
        stocks = StockRepo.search_stock_by_ticker(ticker_search)
        return jsonify(stocks), 200
    except Exception as e:
        logging.exception(e)
        return jsonify({'message', 'could not get stocks'}), 409

@stocks.route('/portfolio/all', methods=['GET'])
def get_all_stocks():
    try:
        stocks = StockRepo.get_all_stocks()
        return jsonify(stocks), 200
    except Exception as e:
        logging.exception(e)
        return jsonify({'message', 'could not get stocks'}), 409

@stocks.route('/portfolio', methods=['POST'])
def add_stock():
    # TODO: add logic to calculate and adjust cash flow from given account
    try:
        data = request.json
        ticker = data['ticker'].upper()
        data['ticker'] = ticker
        price_res = requests.get(
            f'https://api.twelvedata.com/price?symbol={ticker}&apikey={os.environ["TWELVE_API_KEY"]}'
        ).json()
        amount = float(price_res['price'])*int(data['quantity'])
        data['amount_invested'] = amount
        new_stock = Stock(**data)
        StockRepo.add_new_stock(new_stock)
        #Update account state and flows due to stock addition
        update_flows(-amount, data['account_no'], data['quantity'], price_res['price'], ticker)
        return jsonify(new_stock), 201
    except InsufficientFundsError as e:
        return jsonify({'message': str(e)}), 400
    except StockAlreadyExistsError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        logging.exception(e)
        return {'message': 'could not insert stock'}, 409


@stocks.route('/portfolio/<ticker>', methods=['DELETE'])
def delete_stock(ticker: str):
    # TODO: add logic to update liquid balance in account
    try:
        ticker = ticker.upper()
        stock = StockRepo.get_stock_by_ticker(ticker)
        price_res = requests.get(
            f'https://api.twelvedata.com/price?symbol={ticker}&apikey={os.environ["TWELVE_API_KEY"]}'
        ).json()
        StockRepo.remove_stock(ticker)
        amount = float(price_res['price'])*int(stock['quantity'])
        update_flows(amount, stock['account_no'], -stock['quantity'], price_res['price'], ticker)
        return jsonify(ticker), 202
    except StockDoesNotExistError as e:
        return jsonify({'message': str(e)})
    except Exception as e:
        logging.exception(e)
        return jsonify({'message': 'could not remove stock'}), 409

@stocks.route('/portfolio', methods=['PUT'])
def update_stock():
    try:
        data = request.json
        ticker = data['ticker'].upper()
        stock = StockRepo.get_stock_by_ticker(ticker)
        price_res = requests.get(
            f'https://api.twelvedata.com/price?symbol={data["ticker"]}&apikey={os.environ["TWELVE_API_KEY"]}'
        ).json()
        amount = float(price_res['price'])*int(data['quantity'])
        flow = float(stock['amount_invested'])-amount
        StockRepo.update_stock(ticker=ticker, quantity=data['quantity'], amount_invested=amount)
        qty_diff = data['quantity']-stock['quantity']
        update_flows(flow, stock['account_no'], qty_diff, price_res['price'], ticker)
        return jsonify(data), 204
    except Exception as e:
        logging.exception(e)
        return {'message': 'could not update stock'}, 409

@stocks.route('/portfolio/returns', methods=['GET'])
def get_total_returns():
    try:
        total_returns = StockRepo.get_total_returns()
        return {'returns': total_returns}, 200
    except Exception as e:
        logging.exception(e)
        return jsonify({'message', 'could not get stocks'}), 409

@stocks.route('/portfolio/returns/<ticker>', methods=['GET'])
def get_returns(ticker: str):
    try:
        stock_returns = StockRepo.get_stock_returns(ticker)
        return jsonify({'returns':stock_returns}), 200
    except StockDoesNotExistError as e:
        return jsonify({'message':str(e)}), 400
    except Exception as e:
        logging.exception(e)
        return jsonify({'message':'Could not get returns'}), 409

@stocks.route('/portfolio/performance', methods=['GET'])
def get_stock_performance():
    #TODO: find api that gives stock performance
    try:
        performance={'gainers':[], 'losers':[]}
        all_stocks = StockRepo.get_all_stocks()
        for stock in all_stocks:
            ticker = stock['ticker']
            stock_quote = requests.get(
                f'https://api.twelvedata.com/quote?symbol={ticker}&apikey={os.environ["TWELVE_API_KEY"]}'
            ).json()
            float_percent = float(stock_quote['percent_change'])
            if float_percent > 0:
                performance['gainers'].append({ticker: float_percent})
            else:
                performance['losers'].append({ticker: float_percent})
            
        performance['gainers'] = sorted(performance['gainers'], key = lambda gainer: float(list(gainer.values())[0]))
        performance['losers'] = sorted(performance['losers'], key = lambda loser: float(list(loser.values())[0]), reverse=True)
        return performance, 200
    except Exception as e:
        logging.exception(e)
        return jsonify({'message', 'could not get stocks'}), 409
