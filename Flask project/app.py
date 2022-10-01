import json
import pandas as pd
from data import WeatherData
from flask import Flask, request, redirect, render_template, url_for

app = Flask(__name__)

# Loading data from the JSON files
def load_data(key: str = "Eindhoven"):
    with open("WeatherData.json", "r") as f:
        data = json.load(f)

    return data[key]


def load_csv(key: str = "Eindhoven"):
    df = pd.read_csv("WeatherData.csv")
    pass


@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        selected = request.form['city']
        return redirect(url_for("stats", city=selected))
    else:
        return render_template("index.html")


@app.route("/update", methods=["GET", "POST"])
def update():
    weather_data = WeatherData()
    weather_data.update_json()
    return redirect(url_for('home'))


@app.route("/stats/<string:city>", methods=["GET", "POST"])
def stats(city):
    data = load_data(key=city)
    # data = load_csv(key=city)
    return render_template("stats.html", city=city, data=data[1], link=data[0])


if __name__ == "__main__":
    app.run(debug=True)
