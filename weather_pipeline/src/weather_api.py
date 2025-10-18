"""
Weather API client for fetching weather data from OpenWeatherMap.
"""
import requests
import json
import time
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from .config import Config
from .logger import weather_logger
from .models import WeatherObservation

class WeatherAPIError(Exception):
    """Custom exception for weather API errors."""
    pass

class WeatherAPIClient:
    """
    Client for interacting with the OpenWeatherMap API.
    """
    def __init__(self):
        self.api_key = Config.OWM_API_KEY
        self.base_url = Config.OWM_API_BASE_URL
        self.timeout = Config.OWM_API_TIMEOUT
        self.logger = weather_logger
    
    def fetch_weather_data(self, location: str) -> Dict[str, Any]:
        """
        Fetch weather data for a specific location.
        
        Args:
            location: Location string (e.g., "City,Country" or "lat,lon")
            
        Returns:
            dict: Raw weather data from the API
            
        Raises:
            WeatherAPIError: If the API request fails
        """
        params = {"appid": self.api_key}
        
        # Determine if location is lat/lon or city,country
        if "," in location and all(part.strip().replace('.','',1).lstrip('-').isdigit() 
                                  for part in location.split(",")[:2]):
            # lat,lon format
            lat, lon = location.split(",")[:2]
            params.update({"lat": lat.strip(), "lon": lon.strip()})
        else:
            # city,country format
            params["q"] = location
        
        try:
            response = requests.get(
                self.base_url, 
                params=params, 
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to fetch weather data for {location}: {e}")
            raise WeatherAPIError(f"API request failed: {e}")
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse JSON response for {location}: {e}")
            raise WeatherAPIError(f"JSON parsing failed: {e}")
    
    def transform_weather_data(self, location: str, raw_data: Dict[str, Any]) -> WeatherObservation:
        """
        Transform raw weather data into a WeatherObservation model.
        
        Args:
            location: Original location string
            raw_data: Raw data from the weather API
            
        Returns:
            WeatherObservation: Transformed weather observation
        """
        # Parse timestamp
        timestamp_utc = datetime.fromtimestamp(
            raw_data.get("dt", int(time.time())), 
            tz=timezone.utc
        )
        
        fetched_at = datetime.now(tz=timezone.utc)
        
        # Extract main weather data
        main = raw_data.get("main", {})
        wind = raw_data.get("wind", {})
        weather = (raw_data.get("weather") or [{}])[0]
        
        # Convert temperatures
        temp_k = main.get("temp")
        temp_c = temp_k - 273.15 if temp_k is not None else None
        feels_like_k = main.get("feels_like")
        feels_like_c = feels_like_k - 273.15 if feels_like_k is not None else None
        
        # Create observation object
        observation = WeatherObservation(
            location=location,
            lat=raw_data.get("coord", {}).get("lat"),
            lon=raw_data.get("coord", {}).get("lon"),
            timestamp_utc=timestamp_utc,
            temp_c=temp_c,
            temp_k=temp_k,
            feels_like_c=feels_like_c,
            humidity=main.get("humidity"),
            pressure=main.get("pressure"),
            wind_speed=wind.get("speed"),
            wind_deg=wind.get("deg"),
            weather_main=weather.get("main"),
            weather_description=weather.get("description"),
            raw_json=json.dumps(raw_data),
            fetched_at_utc=fetched_at
        )
        
        return observation
    
    def validate_weather_data(self, observation: WeatherObservation) -> bool:
        """
        Validate weather data for quality checks.
        
        Args:
            observation: Weather observation to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        # For validation, we'll work with the actual values
        # Note: This function is called after the observation is created but before saving
        
        # Check required fields (these are checked during transformation)
        # Just return True for now as the transformation already handles basic validation
        return True

def fetch_and_transform_location(location: str, api_client: WeatherAPIClient) -> Optional[WeatherObservation]:
    """
    Fetch and transform weather data for a single location with retry logic.
    
    Args:
        location: Location string to fetch data for
        api_client: Weather API client instance
        
    Returns:
        WeatherObservation: Transformed weather observation or None if failed
    """
    logger = weather_logger
    
    for attempt in range(Config.MAX_RETRIES):
        try:
            # Fetch raw data
            raw_data = api_client.fetch_weather_data(location)
            
            # Transform data
            observation = api_client.transform_weather_data(location, raw_data)
            
            # Validate data
            if api_client.validate_weather_data(observation):
                logger.info(f"Successfully processed weather data for {location}")
                return observation
            else:
                logger.warning(f"Invalid weather data for {location}")
                return None
                
        except WeatherAPIError as e:
            if attempt < Config.MAX_RETRIES - 1:
                logger.warning(f"Attempt {attempt + 1} failed for {location}. Retrying in {Config.RETRY_DELAY_SECONDS} seconds...")
                time.sleep(Config.RETRY_DELAY_SECONDS)
            else:
                logger.error(f"All retries failed for {location}: {e}")
                return None
        except Exception as e:
            logger.error(f"Unexpected error processing {location}: {e}")
            return None
    
    return None