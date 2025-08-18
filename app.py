from flask import Flask, render_template, jsonify, request
import pandas as pd
from weather import fetch_weather_data, calculate_pv_power

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def data():
    lat = float(request.args.get("lat", 52.0))
    lon = float(request.args.get("lon", 21.0))
    eta = float(request.args.get("eta", 0.18))
    area = float(request.args.get("area", 10))

    raw = fetch_weather_data(lat, lon)
    hourly = raw["hourly"]
    df = pd.DataFrame({
        "time": pd.to_datetime(hourly["time"]),
        "temperature": hourly["temperature_2m"],
        "irradiance": hourly["shortwave_radiation"],
        "windspeed": hourly["windspeed_10m"],
    })
    df["pv_power"] = df["irradiance"].apply(lambda g: calculate_pv_power(g, eta, area)).round(2)
    df["pv_energy_kwh"] = (df["pv_power"] / 1000).round(2)

    total_energy = round(df["pv_energy_kwh"].sum(), 2)

    df["date"] = df["time"].dt.date
    #df = df.drop(columns=["time"])
    summary = df.groupby("date").agg({
        "pv_energy_kwh": "sum",
        "irradiance": "mean",
        "windspeed": "mean",
        "temperature": "mean"
    }).reset_index().round(2)
    df = df.drop(columns=["date"])
    df = df[["time", "temperature", "irradiance", "windspeed", "pv_power", "pv_energy_kwh" ]]
    print(df.head())
    return jsonify({
        "records": df.to_dict(orient="records"),
        "summary": summary.to_dict(orient="records"),
        "total_energy": total_energy
    })

if __name__ == "__main__":
    app.run(debug=True)