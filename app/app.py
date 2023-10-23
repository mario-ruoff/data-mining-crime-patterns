from flask import Flask, render_template
from dotenv import load_dotenv
import os
from database.clusters import ChicagoCrimes

# Initialize app
load_dotenv()
app = Flask(__name__)
title = "Chicago Crime Map"
data = ChicagoCrimes('../database/crimes.db')

# Set up main route
@app.route("/")
def load_map():
    return render_template(
        "map.html",
        title=title,
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        center=(41.87820816040039, -87.62979125976562),
        zoom=10,
        heatmap=data.get_crimes(),
        police_stations=data.get_police_stations(),
        presence_predictions=[
            (41.8782, -87.6297),
            (41.7782, -87.6297),
            (41.8382, -87.6897),
            (41.9182, -87.7097),
            (41.7982, -87.6497),
            (41.8582, -87.6697),
            (41.9082, -87.6697),
        ],
    )