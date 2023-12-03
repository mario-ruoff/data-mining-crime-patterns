from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
from database.clusters import ChicagoCrimes

# Initialize app
load_dotenv()
app = Flask(__name__)
title = "Chicago Crime Map"
current_year = 2023
min_year = 2001
data = ChicagoCrimes('../database/crimes.db')
stations = data.get_police_stations()
crime_types = data.get_crime_types()
n_clusters = len(stations)

if(len(crime_types) > 1): 
    num_crimes = 10000
else:
    num_crimes = 0

crimes, clusters = data.get_crimes(crime_types=crime_types, k=n_clusters, year=current_year, num_crimes=num_crimes)

# Set up main route
@app.route("/")
def load_map():
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
        crime_types=crime_types,
        heatmap=crimes,
        police_stations=stations,
        presence_predictions=clusters,
        current_year=current_year,
        min_year=min_year,
        n_clusters=n_clusters
    )

# Create route to filter by different parameters
@app.route("/api/filter")
def filter():
    crime_types = request.args.getlist("crime_types[]")
    year = request.args.get("year", 0 , type=int)
    n_clusters = request.args.get("n_clusters", 0 , type=int)
    crimes, clusters = data.get_crimes(crime_types=crime_types, year=year, k=n_clusters)
    print(clusters)
    
    return {
        "crimes": crimes,
        "clusters": clusters.tolist() if clusters is not None else []
    }
