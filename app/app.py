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
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        center="41.87820816040039,-87.62979125976562",
        title=title
    )