from flask import Flask
from dotenv import load_dotenv
import os

# Initialize app
load_dotenv()
app = Flask(__name__)

# Set up main route
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"