import requests

def fetch_weather_data(lat=52.0, lon=21.0):
    url = (
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
        "&hourly=temperature_2m,shortwave_radiation,windspeed_10m&timezone=auto"
    )
    response = requests.get(url)
    data = response.json()
    return data

def calculate_pv_power(irradiance, eta=0.18, area=10):
    return irradiance * eta * area
