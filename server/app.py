from flask import Flask

from controller.stock_controller import stocks

app = Flask(__name__)

app.register_blueprint(stocks, url_prefix='/stocks')

if __name__ == '__main__':
    app.run(debug=True)
