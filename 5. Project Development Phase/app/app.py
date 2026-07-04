"""
Rising Waters - Flood Prediction Web Application
--------------------------------------------------
Flask app that loads the trained model + scaler bundle (floods.save) produced
by the Jupyter notebook and serves an interactive flood risk prediction tool.

Pages:
    /            Home page
    /predict     Prediction input page (GET: show form, POST: run prediction)
    /result      Flood Chance / No Flood Chance result page (rendered after POST)

Run with:
    python app.py
Then open http://127.0.0.1:5000
"""
import os

import joblib
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "model", "floods.save")

app = Flask(__name__)

# ---------------------------------------------------------------------
# Load the trained model + scaler bundle once at startup
# ---------------------------------------------------------------------
_bundle = joblib.load(MODEL_PATH)
MODEL = _bundle["model"]
SCALER = _bundle["scaler"]
FEATURE_NAMES = _bundle["feature_names"]
MODEL_NAME = _bundle["model_name"]
MODEL_ACCURACY = _bundle["accuracy"]

import json
with open("features.json", "w") as f:
    json.dump(FEATURE_NAMES, f)

# Field metadata used to render the prediction form (label, unit, helper text,
# a sensible default and a min/max for the number input)
FIELD_META = {
    "Temp":        {"label": "Temperature",        "unit": "°C",  "step": "0.1", "min": -10, "max": 55,
                     "help": "Average air temperature for the period", "default": 29},
    "Humidity":    {"label": "Humidity",            "unit": "%",   "step": "0.1", "min": 0,   "max": 100,
                     "help": "Relative humidity reading", "default": 73},
    "Cloud Cover": {"label": "Cloud Cover",         "unit": "%",   "step": "0.1", "min": 0,   "max": 100,
                     "help": "Sky cloud cover / visibility obstruction", "default": 36},
    "ANNUAL":      {"label": "Annual Rainfall",     "unit": "mm",  "step": "0.1", "min": 0,   "max": 8000,
                     "help": "Total rainfall recorded for the year", "default": 3000},
    "Jan-Feb":     {"label": "Jan\u2013Feb Rainfall", "unit": "mm", "step": "0.1", "min": 0,   "max": 1500,
                     "help": "Winter season rainfall total", "default": 30},
    "Mar-May":     {"label": "Mar\u2013May Rainfall", "unit": "mm", "step": "0.1", "min": 0,   "max": 2000,
                     "help": "Pre-monsoon season rainfall total", "default": 330},
    "Jun-Sep":     {"label": "Jun\u2013Sep Rainfall", "unit": "mm", "step": "0.1", "min": 0,   "max": 5000,
                     "help": "Monsoon season rainfall total \u2014 the strongest flood predictor", "default": 2100},
    "Oct-Dec":     {"label": "Oct\u2013Dec Rainfall", "unit": "mm", "step": "0.1", "min": 0,   "max": 2000,
                     "help": "Post-monsoon / retreating monsoon rainfall", "default": 520},
    "avgjune":     {"label": "Average June Rainfall", "unit": "mm", "step": "0.1", "min": 0, "max": 1000,
                     "help": "average of June rainfall", "default": 220},
    "sub":         {"label": "Sub-total Index",     "unit": "mm",  "step": "0.1", "min": 0,   "max": 1500,
                     "help": "Derived seasonal rainfall sub-total indicator", "default": 440},
}


@app.context_processor
def inject_model_meta():
    return {
        "global_model_name": MODEL_NAME,
        "global_accuracy": round(MODEL_ACCURACY * 100, 2),
    }


FIELD_GROUPS = [
    ("Atmospheric Readings", ["Temp", "Humidity", "Cloud Cover"]),
    ("Seasonal Rainfall", ["Jan-Feb", "Mar-May", "Jun-Sep", "Oct-Dec"]),
    ("Derived Rainfall Indicators", ["ANNUAL", "avgjune", "sub"]),
]


@app.route("/")
def home():
    return render_template(
        "home.html",
        model_name=MODEL_NAME,
        accuracy=round(MODEL_ACCURACY * 100, 2),
        n_features=len(FEATURE_NAMES),
    )


@app.route("/hero_image")
def hero_image():
    from flask import redirect
    # Serve the hero flood image from a hosted URL
    return redirect("https://www.pbs.org/wgbh/nova/media/images/katrina-flooding.width-2000.jpg")





@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "GET":
        return render_template("predict.html", groups=FIELD_GROUPS, meta=FIELD_META, errors=None, values={})

    # POST: parse + validate inputs
    values = {}
    errors = {}
    for f in FEATURE_NAMES:
        raw = request.form.get(f, "").strip()
        try:
            values[f] = float(raw)
        except ValueError:
            errors[f] = "Enter a valid number."

    if errors:
        return render_template("predict.html", groups=FIELD_GROUPS, meta=FIELD_META,
                                errors=errors, values=request.form)

    ordered = pd.DataFrame([[values[f] for f in FEATURE_NAMES]], columns=FEATURE_NAMES)
    scaled = SCALER.transform(ordered)

    pred = int(MODEL.predict(scaled)[0])
    try:
        proba = MODEL.predict_proba(scaled)[0]
        flood_probability = float(proba[1]) * 100
    except AttributeError:
        flood_probability = 100.0 if pred == 1 else 0.0

    template = "flood_result.html" if pred == 1 else "no_flood_result.html"
    return render_template(
        template,
        probability=round(flood_probability, 1),
        values=values,
        meta=FIELD_META,
        model_name=MODEL_NAME,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
