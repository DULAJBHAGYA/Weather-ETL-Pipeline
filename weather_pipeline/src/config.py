"""
Configuration management for the Weather ETL Pipeline.
"""
import os
from dotenv import load_dotenv
from typing import List, Optional

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Configuration class for the Weather ETL Pipeline.
    """
    # OpenWeather API Configuration
    OWM_API_KEY: str = os.getenv("OWM_API_KEY", "")
    LOCATIONS: List[str] = os.getenv("LOCATIONS", "Colombo,Sri Lanka;Kandy,Sri Lanka;Anuradhapura,Sri Lanka;London,UK").split(";")
    
    # Database Configuration
    SQLITE_DB: str = os.getenv("SQLITE_DB", "./db/weather.db")
    
    # S3 Configuration (optional)
    S3_BUCKET: Optional[str] = os.getenv("S3_BUCKET")
    PUSH_TO_S3: bool = os.getenv("PUSH_TO_S3", "false").lower() == "true"
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "./logs/pipeline.log")
    
    # Scheduler Configuration
    SCHEDULE_INTERVAL_HOURS: int = int(os.getenv("SCHEDULE_INTERVAL_HOURS", "1"))
    
    # Retry Configuration
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    RETRY_DELAY_SECONDS: int = int(os.getenv("RETRY_DELAY_SECONDS", "5"))
    
    # Data Validation
    MIN_TEMP_C: float = float(os.getenv("MIN_TEMP_C", "-100"))
    MAX_TEMP_C: float = float(os.getenv("MAX_TEMP_C", "100"))
    
    # API Configuration
    OWM_API_TIMEOUT: int = int(os.getenv("OWM_API_TIMEOUT", "20"))
    OWM_API_BASE_URL: str = "https://api.openweathermap.org/data/2.5/weather"
    
    @classmethod
    def validate(cls) -> bool:
        """
        Validate required configuration values.
        
        Returns:
            bool: True if all required configurations are present, False otherwise
        """
        if not cls.OWM_API_KEY:
            raise ValueError("OWM_API_KEY is required. Please set it in your .env file.")
        
        if not cls.LOCATIONS:
            raise ValueError("LOCATIONS is required. Please set it in your .env file.")
        
        return True
    
    @classmethod
    def get_database_url(cls) -> str:
        """
        Get the database URL for SQLAlchemy.
        
        Returns:
            str: Database URL
        """
        return f"sqlite:///{cls.SQLITE_DB}"

# Validate configuration on import
try:
    Config.validate()
except ValueError as e:
    print(f"Configuration Error: {e}")