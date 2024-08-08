from flask import Flask
from load_dotenv import load_dotenv

from controller.stock_controller import stocks
<<<<<<< Updated upstream
from controller.value_controller import value

load_dotenv('.env')
=======
from controller.mutual_funds_controller import mutual_funds
>>>>>>> Stashed changes

app = Flask(__name__)

app.register_blueprint(stocks, url_prefix='/stocks')
<<<<<<< Updated upstream
app.register_blueprint(value, url_prefix='/value')
=======
app.register_blueprint(mutual_funds, url_prefix='/mutual_funds')
>>>>>>> Stashed changes

if __name__ == '__main__':
    app.run(debug=True)
