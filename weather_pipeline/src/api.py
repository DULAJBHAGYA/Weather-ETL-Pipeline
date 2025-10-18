"""
Simple Flask API to serve weather data to the frontend dashboard.
"""
from flask import Flask, jsonify
import json
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from config import Config
from models import DatabaseManager, WeatherObservation

app = Flask(__name__)
db_manager = DatabaseManager(Config.get_database_url())

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "timestamp": "2025-10-18T18:01:14.325568"
    })

@app.route('/api/weather/latest', methods=['GET'])
def get_latest_weather():
    """Get the latest weather data for all locations."""
    try:
        session = db_manager.get_session()
        try:
            # Get all locations
            locations = session.query(WeatherObservation.location).distinct().all()
            locations = [loc[0] for loc in locations]
            
            weather_data = []
            
            # Get the latest observation for each location
            for location in locations:
                observation = session.query(WeatherObservation).filter(
                    WeatherObservation.location == location
                ).order_by(WeatherObservation.fetched_at_utc.desc()).first()
                
                if observation:
                    # Use the to_dict method to get the data
                    obs_dict = observation.to_dict()
                    
                    # Parse the raw JSON to get visibility and other detailed data
                    raw_json = obs_dict.get('raw_json')
                    raw_data = json.loads(raw_json) if raw_json else {}
                    
                    weather_data.append({
                        "id": obs_dict.get("id"),
                        "location": obs_dict.get("location"),
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
            
            # Filter for the locations we want to display (Sri Lanka locations)
            sri_lanka_locations = [d for d in weather_data if "Sri Lanka" in d["location"]]
            # Extract just the city name for display
            filtered_data = []
            for d in sri_lanka_locations:
                # Create a copy with just the city name
                new_entry = d.copy()
                location_name = d["location"]
                if location_name:
                    new_entry["location"] = location_name.split(",")[0]  # Just the city part
                else:
                    new_entry["location"] = "Unknown"
                filtered_data.append(new_entry)
            
            return jsonify(filtered_data)
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
            # Get the latest observation for the specified location
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
            
            location_name = obs_dict.get("location")
            if location_name:
                city_name = location_name.split(",")[0]  # Just the city part
            else:
                city_name = "Unknown"
            
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
    app.run(host='0.0.0.0', port=5000, debug=True)