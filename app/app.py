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
    stations = data.get_police_stations()
    crimes, clusters = data.get_crimes()
    
    return render_template(
        "map.html",
        title=title,
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        center=(41.87820816040039, -87.62979125976562),
        zoomLevel=12,
        zoomLevelMax=22,
        zoomLevelMin=10,
        heatmapRadius=20,
        heatmapRadiusMin=0,
        heatmapRadiusMax=100,
        heatmap=crimes,
        police_stations=stations,
        presence_predictions=clusters
    )