import matplotlib.pyplot as plt
import numpy as np
import os
import time

from flask import Flask, render_template, request
from dotenv import load_dotenv
from database.data_manager import ChicagoCrimes

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
DEBUG = False

algorithms = dict({1: "KMeans", 2: "Spectral", 3: "DBSCAN"})

# This section of code is not run when the application is running. It's to help provide metrics for the report.
if DEBUG:
    x = []
    y = []
    for a in algorithms:
        algorithm = algorithms[a]
        start_time = time.time()
        crimes, clusters = data.get_crimes(crime_types=crime_types, k=n_clusters, year=2022, algorithm=a)
        end_time = time.time()
        x.append(algorithm)
        y.append(np.round(end_time - start_time, decimals=2))
    
    figure, axis = plt.subplots()
    bar_colors = ['tab:red', 'tab:blue', 'tab:green']
    axis.bar(x, y, color=bar_colors)

    axis.set_ylabel('Time to cluster (seconds)')
    axis.set_title('Performance Evaluation of different clustering algorithms.')
    plt.show()
    plt.savefig('./fig.png')

    exit()

crimes, clusters = data.get_crimes(crime_types=[crime_types[0]], k=n_clusters, year=current_year)

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
    algorithm = int(request.args.get("algorithm", "", type=str)[-1])
    year = request.args.get("year", 0 , type=int)
    n_clusters = request.args.get("n_clusters", 0 , type=int)
    crimes, clusters = data.get_crimes(crime_types=crime_types, year=year, k=n_clusters, algorithm=algorithm)
    
    return {
        "crimes": crimes,
        "clusters": clusters.tolist()
    }
