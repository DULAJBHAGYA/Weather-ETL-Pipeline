"""
Simple Flask API to serve weather data for Kandy, Colombo, and Anuradhapura
to the frontend dashboard.
"""
from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(__file__))

# Import our existing modules
from src.config import Config
from src.models import DatabaseManager, WeatherObservation
import json

app = Flask(__name__)
# Enable CORS for all routes
CORS(app)

# Initialize database manager
db_manager = DatabaseManager(Config.get_database_url())

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/api/weather/latest', methods=['GET'])
def get_latest_weather():
    """Get the latest weather data for Kandy, Colombo, and Anuradhapura."""
    try:
        session = db_manager.get_session()
        try:
            # Define the locations we want to display
            target_locations = ["Kandy", "Colombo", "Anuradhapura"]
            weather_data = []
            
            # Get the latest observation for each target location
            for location in target_locations:
                # Look for locations that start with our target (to match "Colombo,Sri Lanka")
                observation = session.query(WeatherObservation).filter(
                    WeatherObservation.location.like(f"{location}%")
                ).order_by(WeatherObservation.fetched_at_utc.desc()).first()
                
                if observation:
                    # Use the to_dict method to get the data
                    obs_dict = observation.to_dict()
                    
                    # Parse the raw JSON to get visibility and other detailed data
                    raw_json = obs_dict.get('raw_json')
                    raw_data = json.loads(raw_json) if raw_json else {}
                    
                    # Extract just the city name (remove country)
                    full_location = obs_dict.get("location", "")
                    city_name = full_location.split(",")[0] if "," in full_location else full_location
                    
                    weather_data.append({
                        "id": obs_dict.get("id"),
                        "location": city_name,
                        "timestamp": obs_dict.get("timestamp_utc"),
                        "temperature_celsius": obs_dict.get("temp_c"),
                        "feels_like_celsius": obs_dict.get("feels_like_c"),
                        "humidity_percent": obs_dict.get("humidity"),
                        "pressure_hpa": obs_dict.get("pressure"),
                        "wind_speed_ms": obs_dict.get("wind_speed"),
                        "visibility_meters": raw_data.get("visibility", 10000),  # Default to 10km if not available
                        "weather_main": obs_dict.get("weather_main"),
                        "weather_description": obs_dict.get("weather_description"),
                        "clouds_percent": raw_data.get("clouds", {}).get("all", 0),
                        "rain_1h_mm": raw_data.get("rain", {}).get("1h", None),
                        "snow_1h_mm": raw_data.get("snow", {}).get("1h", None)
                    })
            
            return jsonify(weather_data)
        finally:
            session.close()
    except Exception as e:
        print(f"Error fetching latest weather data: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/weather/<location>', methods=['GET'])
def get_weather_by_location(location):
    """Get the latest weather data for a specific location."""
    try:
        session = db_manager.get_session()
        try:
            # Look for locations that start with our target
            observation = session.query(WeatherObservation).filter(
                WeatherObservation.location.like(f"{location}%")
            ).order_by(WeatherObservation.fetched_at_utc.desc()).first()
            
            if not observation:
                return jsonify({"error": f"No data found for location: {location}"}), 404
            
            # Use the to_dict method to get the data
            obs_dict = observation.to_dict()
            
            # Parse the raw JSON to get visibility and other detailed data
            raw_json = obs_dict.get('raw_json')
            raw_data = json.loads(raw_json) if raw_json else {}
            
            # Extract just the city name (remove country)
            full_location = obs_dict.get("location", "")
            city_name = full_location.split(",")[0] if "," in full_location else full_location
            
            weather_data = {
                "id": obs_dict.get("id"),
                "location": city_name,
                "timestamp": obs_dict.get("timestamp_utc"),
                "temperature_celsius": obs_dict.get("temp_c"),
                "feels_like_celsius": obs_dict.get("feels_like_c"),
                "humidity_percent": obs_dict.get("humidity"),
                "pressure_hpa": obs_dict.get("pressure"),
                "wind_speed_ms": obs_dict.get("wind_speed"),
                "visibility_meters": raw_data.get("visibility", 10000),  # Default to 10km if not available
                "weather_main": obs_dict.get("weather_main"),
                "weather_description": obs_dict.get("weather_description"),
                "clouds_percent": raw_data.get("clouds", {}).get("all", 0),
                "rain_1h_mm": raw_data.get("rain", {}).get("1h", None),
                "snow_1h_mm": raw_data.get("snow", {}).get("1h", None)
            }
            
            return jsonify(weather_data)
        finally:
            session.close()
    except Exception as e:
        print(f"Error fetching weather data for {location}: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)