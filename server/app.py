from flask import Flask
from flask_cors import CORS
from load_dotenv import load_dotenv

from controller.stock_controller import stocks
from controller.value_controller import value
from controller.account_controller import account
from controller.mutual_funds_controller import mutual_funds

load_dotenv('.env')


app = Flask(__name__)
CORS(app=app, origins=['*'])

app.register_blueprint(stocks, url_prefix='/stocks')
app.register_blueprint(value, url_prefix='/value')
app.register_blueprint(mutual_funds, url_prefix='/mutual_funds')
app.register_blueprint(account, url_prefix='/accounts')

if __name__ == '__main__':
    app.run(debug=True)
