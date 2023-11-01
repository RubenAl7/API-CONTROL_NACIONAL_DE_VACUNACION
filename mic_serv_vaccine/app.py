from flask import Flask, render_template
from dotenv import load_dotenv
import os

from config.mongodb import mongo
from routes.vacc import vaccine 

load_dotenv()

# APP
app = Flask(__name__)


app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo.init_app(app)

@app.route('/')  # home page route
def index():
    return render_template('index.html')


app.register_blueprint(vaccine, url_prefix='/vaccine')


if __name__ == '__main__':
    app.run(debug=True)


