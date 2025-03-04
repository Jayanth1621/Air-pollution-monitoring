import requests
import dash
from dash import dcc, html
from flask import Flask

# Set up Flask and Dash
server = Flask(__name__)
app = dash.Dash(__name__, server=server)

# Weather API Configuration
API_KEY = "47ff008fcae3f390c655209a66ad27a1"  # Replace with your OpenWeatherMap API key
CITY = "Ramanagara"
#URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
# lat = 12.7258
# lon = 77.2813


def get_weather():
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        return {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"].title(),
            "wind_speed": data["wind"]["speed"]
        }
    return None

def get_cordinates():
    URL = f"http://api.openweathermap.org/geo/1.0/direct?q={CITY}&appid={API_KEY}"
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        return {
            "lat": int(data[0]["lat"]),
            "lon": int(data[0]["lon"])
        }
    return None

def get_air_pollution_info(cords):
    lat = int(cords["lat"])
    lon = int(cords["lon"])
    URL = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        return {
            "aqi": data["list"][0]["main"]["aqi"],
            "pm2_5": data["list"][0]["components"]["pm2_5"],
            "pm10": data["list"][0]["components"]["pm10"],
            "o3": data["list"][0]["components"]["o3"],
            "so2": data["list"][0]["components"]["so2"],
            "no2": data["list"][0]["components"]["no2"],
            "co": data["list"][0]["components"]["co"]
        }
    return None

def check_air_quality(aqi: int):
    match aqi:
        case 1:
            return "Good"
        case 2:
            return "Fair"
        case 3:
            return "Moderate"
        case 4:
            return "Poor"
        case 5:
            return "Very Poor"
        case _:
            return "Unknown"
    
cords = get_cordinates()
print(cords)

#weather_data = get_weather()

air_pollution_data = get_air_pollution_info(cords)

print(cords)

quality = check_air_quality(air_pollution_data['aqi'])

print(cords)







# Dash Layout
# app.layout = html.Div([
#     html.H1("Weather Dashboard", style={'textAlign': 'center'}),
#     html.H3(f"City: {weather_data['city']}", style={'textAlign': 'center'}),
#     html.P(f"Temperature: {weather_data['temperature']}°C"),
#     html.P(f"Humidity: {weather_data['humidity']}%"),
#     html.P(f"Weather: {weather_data['description']}"),
#     html.P(f"Wind Speed: {weather_data['wind_speed']} m/s"),
# ])

app.layout = html.Div([
    html.H1("Air Pollution Dashboard", style={'textAlign': 'center'}),
    html.H3(f"City: {CITY}", style={'textAlign': 'center'}),
    html.P(f"AQI: {air_pollution_data['aqi']}"),
    html.P(f"PM2.5: {air_pollution_data['pm2_5']} µg/m³"),
    html.P(f"PM10: {air_pollution_data['pm10']} µg/m³"),
    html.P(f"O3: {air_pollution_data['o3']} µg/m³"),
    html.P(f"SO2: {air_pollution_data['so2']} µg/m³"),
    html.P(f"NO2: {air_pollution_data['no2']} µg/m³"),
    html.P(f"CO: {air_pollution_data['co']} µg/m³"),

    html.P(f"Air Quality: {quality}")
])



if __name__ == '__main__':
    app.run_server(debug=True)
