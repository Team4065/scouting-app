from flask import Flask
from markupsafe import escape
import dotenv
from app.database import db

dotenv.load_dotenv('.env', verbose=True) # Load environment variables from .env

app = Flask(__name__)

@app.route('/', defaults={'id': ''})
@app.route('/<id>')
def hello_world(id=''):
    return f'Hello, Hunter! {id}'

@app.route('/home')
def home():
    return 'Home'