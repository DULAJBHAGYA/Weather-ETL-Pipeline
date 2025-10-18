"""
Script to populate the database with sample weather data for testing Grafana integration.
"""
import os
import sys
import sqlite3
from datetime import datetime, timedelta
import random

# Add the project root to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.config import Config

def populate_sample_data():
    """Populate the database with sample weather data."""
    db_path = Config.SQLITE_DB
    print(f"Populating database: {db_path}")
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Sample locations
    locations = [
        "Colombo,Sri Lanka",
        "London,UK",
        "New York,US",
        "Tokyo,Japan",
        "Sydney,Australia"
    ]
    
    # Generate sample data for the last 7 days
    base_time = datetime.utcnow()
    
    insert_data = []
    for day in range(7):
        for hour in range(24):
            for location in locations:
                # Create a timestamp for this data point
                timestamp = base_time - timedelta(days=day, hours=hour)
                
                # Generate realistic weather data
                temp_c = random.uniform(15, 35)  # Temperature in Celsius
                temp_k = temp_c + 273.15  # Temperature in Kelvin
                feels_like_c = temp_c + random.uniform(-2, 2)  # Feels like temperature
                humidity = random.randint(30, 90)  # Humidity percentage
                pressure = random.randint(990, 1030)  # Pressure in hPa
                wind_speed = random.uniform(0, 15)  # Wind speed in m/s
                wind_deg = random.randint(0, 360)  # Wind direction in degrees
                weather_main = random.choice(["Clear", "Clouds", "Rain", "Drizzle", "Thunderstorm"])
                weather_description = random.choice([
                    "clear sky", "few clouds", "scattered clouds", "broken clouds",
                    "light rain", "moderate rain", "heavy intensity rain",
                    "light thunderstorm", "thunderstorm with light rain"
                ])
                
                # Create raw JSON (simplified)
                raw_json = f'{{"temp": {temp_k}, "humidity": {humidity}, "pressure": {pressure}}}'
                
                # Fetched at timestamp
                fetched_at = timestamp + timedelta(minutes=random.randint(0, 10))
                
                insert_data.append((
                    location,
                    round(random.uniform(-90, 90), 6),  # lat
                    round(random.uniform(-180, 180), 6),  # lon
                    timestamp.isoformat(),
                    round(temp_c, 2),
                    round(temp_k, 2),
                    round(feels_like_c, 2),
                    humidity,
                    pressure,
                    round(wind_speed, 2),
                    wind_deg,
                    weather_main,
                    weather_description,
                    raw_json,
                    fetched_at.isoformat()
                ))
    
    # Insert data into the database
    cursor.executemany('''
        INSERT INTO weather_observations (
            location, lat, lon, timestamp_utc, temp_c, temp_k, feels_like_c,
            humidity, pressure, wind_speed, wind_deg, weather_main,
            weather_description, raw_json, fetched_at_utc
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', insert_data)
    
    # Commit and close
    conn.commit()
    conn.close()
    
    print(f"Inserted {len(insert_data)} sample records into the database.")

if __name__ == "__main__":
    populate_sample_data()