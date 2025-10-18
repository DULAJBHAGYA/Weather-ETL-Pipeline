"""
Logging and monitoring utilities for the Weather ETL Pipeline.
"""
import logging
import os
from typing import Optional
from datetime import datetime
from .config import Config

class WeatherLogger:
    """
    Custom logger for the Weather ETL Pipeline.
    """
    def __init__(self, log_file: Optional[str] = None, log_level: str = "INFO"):
        """
        Initialize the logger.
        
        Args:
            log_file: Path to the log file
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.log_file = log_file or Config.LOG_FILE
        self.log_level = log_level
        
        # Ensure log directory exists
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s | %(levelname)s | %(name)s:%(funcName)s:%(lineno)d | %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
    
    def info(self, message: str):
        """Log an info message."""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log a warning message."""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log an error message."""
        self.logger.error(message)
    
    def debug(self, message: str):
        """Log a debug message."""
        self.logger.debug(message)
    
    def critical(self, message: str):
        """Log a critical message."""
        self.logger.critical(message)
    
    def exception(self, message: str):
        """Log an exception with traceback."""
        self.logger.exception(message)

def monitor_data_freshness(db_manager) -> dict:
    """
    Monitor data freshness and return a health report.
    
    Args:
        db_manager: Database manager instance
        
    Returns:
        dict: Health report with stale locations
    """
    logger_instance = WeatherLogger()
    try:
        stale_locations = db_manager.get_stale_locations(minutes_threshold=90)
        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "stale_locations": [
                {"location": row[0], "last_fetch": str(row[1]) if row[1] else None} 
                for row in stale_locations
            ]
        }
        
        if stale_locations:
            logger_instance.warning(f"Stale data detected for {len(stale_locations)} locations")
        
        return report
    except Exception as e:
        logger_instance.error(f"Error monitoring data freshness: {e}")
        return {"error": str(e)}

# Global logger instance
weather_logger = WeatherLogger(Config.LOG_FILE, Config.LOG_LEVEL)