from flask import Flask
from load_dotenv import load_dotenv

from controller.stock_controller import stocks
from controller.value_controller import value
from controller.account_controller import account

load_dotenv('.env')

app = Flask(__name__)

app.register_blueprint(stocks, url_prefix='/stocks')
app.register_blueprint(value, url_prefix='/value')
app.register_blueprint(account, url_prefix='/accounts')

if __name__ == '__main__':
    app.run(debug=True)
