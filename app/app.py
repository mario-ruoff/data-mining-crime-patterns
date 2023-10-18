from flask import Flask, render_template
from dotenv import load_dotenv
import os

# Initialize app
load_dotenv()
app = Flask(__name__)
title = "Chicago Crime Map"

# Set up main route
@app.route("/")
def load_map():
    return render_template(
        "map.html",
        title=title,
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        center=(41.87820816040039, -87.62979125976562),
        zoom=10,
        heatmap=[
            (41.87820816040039, -87.62979125976562),
            (41.77820816040039, -87.62979125976562),
            (41.8382, -87.6897),
            (41.9182, -87.7097),
            (41.7982, -87.6497),
            (41.8582, -87.6697),
            (41.9082, -87.6697),
        ],
        police_stations=[
            (41.8982, -87.6097),
            (41.9382, -87.6397),
            (41.9082, -87.7797),
            (41.7682, -87.6397),
            (41.8482, -87.6497),
        ],
    )