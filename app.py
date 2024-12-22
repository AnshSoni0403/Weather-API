from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # Enable CORS to allow cross-origin requests

# OpenWeatherMap API key
API_KEY = "bf096df206cd6a6f5244af2a9e9037a3"  # Replace with your API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Root route (optional)
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Weather API"})

# Option 1: Handle POST request (Send city data in body)
@app.route('/weather', methods=['POST'])
def get_weather_post():
    data = request.json  # Get JSON data from the request
    city = data.get("city")  # Extract city name

    if not city:
        return jsonify({"error": "City name is required"}), 400

    try:
        # Make a request to the OpenWeatherMap API
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"  # Use "imperial" for Fahrenheit
        }
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise an error for bad status codes

        weather_data = response.json()
        # Extract relevant data
        weather_description = weather_data["weather"][0]["description"]
        temperature = weather_data["main"]["temp"]

        # Return the weather data as JSON
        return jsonify({
            "city": city,
            "temperature": temperature,
            "description": weather_description.capitalize()
        })

    except requests.exceptions.HTTPError:
        return jsonify({"error": "Invalid city name or API error."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Option 2: Handle GET request (City name from URL parameters)
@app.route('/weather', methods=['GET'])
def get_weather_get():
    city = request.args.get('city')  # Extract city name from the query string

    if not city:
        return jsonify({"error": "City name is required"}), 400

    try:
        # Make a request to the OpenWeatherMap API
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"  # Use "imperial" for Fahrenheit
        }
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise an error for bad status codes

        weather_data = response.json()
        # Extract relevant data
        weather_description = weather_data["weather"][0]["description"]
        temperature = weather_data["main"]["temp"]

        # Return the weather data as JSON
        return jsonify({
            "city": city,
            "temperature": temperature,
            "description": weather_description.capitalize()
        })

    except requests.exceptions.HTTPError:
        return jsonify({"error": "Invalid city name or API error."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
