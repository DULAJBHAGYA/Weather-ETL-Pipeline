"""
Script to create a sample Grafana dashboard for weather data.
This script generates a JSON dashboard that can be imported into Grafana.
"""
import json
import os

def create_sample_dashboard():
    """Create a sample Grafana dashboard for weather data."""
    
    dashboard = {
        "dashboard": {
            "id": None,
            "title": "Weather Data Dashboard",
            "tags": ["weather", "etl", "monitoring"],
            "timezone": "browser",
            "schemaVersion": 16,
            "version": 0,
            "refresh": "5m",
            "panels": [
                {
                    "id": 1,
                    "type": "graph",
                    "title": "Temperature Trends",
                    "gridPos": {"x": 0, "y": 0, "w": 12, "h": 9},
                    "datasource": "Weather Data",
                    "targets": [
                        {
                            "rawSql": "SELECT timestamp_utc as time, location, temp_c as temperature FROM weather_observations WHERE $__timeFilter(timestamp_utc) ORDER BY timestamp_utc",
                            "format": "time_series"
                        }
                    ],
                    "fieldConfig": {
                        "defaults": {
                            "unit": "celsius"
                        }
                    }
                },
                {
                    "id": 2,
                    "type": "graph",
                    "title": "Humidity Trends",
                    "gridPos": {"x": 12, "y": 0, "w": 12, "h": 9},
                    "datasource": "Weather Data",
                    "targets": [
                        {
                            "rawSql": "SELECT timestamp_utc as time, location, humidity FROM weather_observations WHERE $__timeFilter(timestamp_utc) ORDER BY timestamp_utc",
                            "format": "time_series"
                        }
                    ],
                    "fieldConfig": {
                        "defaults": {
                            "unit": "percent"
                        }
                    }
                },
                {
                    "id": 3,
                    "type": "table",
                    "title": "Current Weather Conditions",
                    "gridPos": {"x": 0, "y": 9, "w": 24, "h": 8},
                    "datasource": "Weather Data",
                    "targets": [
                        {
                            "rawSql": "SELECT location, temp_c as temperature, humidity, pressure, wind_speed FROM weather_observations WHERE timestamp_utc IN (SELECT MAX(timestamp_utc) FROM weather_observations GROUP BY location)",
                            "format": "table"
                        }
                    ],
                    "fieldConfig": {
                        "defaults": {
                            "custom": {
                                "align": "auto"
                            }
                        }
                    }
                }
            ],
            "templating": {
                "list": [
                    {
                        "name": "location",
                        "type": "query",
                        "datasource": "Weather Data",
                        "refresh": 1,
                        "query": "SELECT DISTINCT location FROM weather_observations",
                        "sort": 1,
                        "current": {
                            "text": "All",
                            "value": "$__all"
                        }
                    }
                ]
            },
            "time": {
                "from": "now-24h",
                "to": "now"
            },
            "timepicker": {
                "refresh_intervals": ["5s", "10s", "30s", "1m", "5m", "15m", "30m", "1h", "2h", "1d"],
                "time_options": ["5m", "15m", "1h", "6h", "12h", "24h", "2d", "7d", "30d"]
            }
        },
        "overwrite": True
    }
    
    return dashboard

def save_dashboard_to_file():
    """Save the dashboard to a JSON file."""
    dashboard = create_sample_dashboard()
    
    # Create docs directory if it doesn't exist
    os.makedirs("./docs", exist_ok=True)
    
    # Save to file
    with open("./docs/sample_weather_dashboard.json", "w") as f:
        json.dump(dashboard, f, indent=2)
    
    print("Sample dashboard saved to ./docs/sample_weather_dashboard.json")
    print("You can import this into Grafana by:")
    print("1. Going to Create → Import in Grafana")
    print("2. Uploading this JSON file")
    print("3. Selecting your 'Weather Data' datasource")
    print("4. Clicking Import")

if __name__ == "__main__":
    save_dashboard_to_file()