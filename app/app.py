from flask import Flask
from flask_googlemaps import GoogleMaps
from dotenv import load_dotenv
import os

# Initialize app
app = Flask(__name__)
GoogleMaps(app, key=os.getenv("GOOGLE_API_KEY"))

# Set up main route
@app.route("/")
def hello_world():
    return "<p>Hello, World2!</p>"