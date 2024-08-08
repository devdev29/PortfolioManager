from flask import Flask
from load_dotenv import load_dotenv

from controller.stock_controller import stocks
from controller.value_controller import value

load_dotenv('.env')

app = Flask(__name__)

app.register_blueprint(stocks, url_prefix='/stocks')
app.register_blueprint(value, url_prefix='/value')

if __name__ == '__main__':
    app.run(debug=True)
