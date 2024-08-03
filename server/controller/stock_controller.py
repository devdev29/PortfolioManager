import os
import requests

from flask import Flask, jsonify, request

from model.stock_model import Stock
from repository.stocks_repo import StockRepo

app = Flask(__name__)

STOCK_EXCHANGE = 'BSE'

@app.route('/stocks/search/<ticker_search>', methods=['GET'])
def get_valid_stocks(ticker_search: str):
    ticker_search = ticker_search.upper()
    res = requests.get(
        f'https://financialmodelingprep.com/api/v3/search?query={ticker_search}&exchange={STOCK_EXCHANGE}&limit=5&apikey={os.environ["FMP_API_KEY"]}'
        )
    return res

@app.route('/stocks/portfolio/<ticker_search>', methods=['GET'])
def get_portfolio_stocks(ticker_search: str):
    ticker_search = ticker_search.upper()
    stocks = StockRepo.search_portfolio_stock_by_ticker(ticker_search)
    return jsonify(stocks), 200

@app.route('/stocks/portfolio', methods=['POST'])
def add_stock():
    # TODO: add logic to calculate and adjust cash flow from given account
    data = request.json
    ticker = data['ticker']
    price_res = requests.get(
        f'https://api.twelvedata.com/price?symbol={ticker}&exchange={STOCK_EXCHANGE}&apikey={os.environ["TWELVE_API_KEY"]}'
    ).json()
    amount = price_res['price']*data['quantity']
    data['amount_invested'] = amount
    new_stock = Stock(**data)
    added = StockRepo.add_new_stock(new_stock)
    if added == 1:
        return jsonify(new_stock), 200
    return {'message': 'could not insert stock'}, 500


@app.route('/stocks/portfolio/<ticker>', methods=['DELETE'])
def delete_stock(ticker: str):
    # TODO: add logic to update liquid balance in account
    res = StockRepo.remove_stock(ticker)
    if res == 1:
        return jsonify(ticker), 200
    return {'message': 'could not remove stock'}, 500

@app.route('/stocks/portfolio', methods=['PUT'])
def update_stock():
    data = request.json
    price_res = requests.get(
        f'https://api.twelvedata.com/price?symbol={data['ticker']}&exchange={STOCK_EXCHANGE}&apikey={os.environ["TWELVE_API_KEY"]}'
    ).json()
    amount = price_res['price']*data['quantity']
    data['amount_invested'] = amount
    stock = Stock(**data)
    res = StockRepo.update_stock(stock=stock)
    if res == 1:
        return jsonify(stock), 200
    return {'message': 'could not update stock'}, 500
