"""
Main ETL pipeline for the Weather Data Pipeline.
"""
import json
import time
from typing import List, Optional
from datetime import datetime
from tqdm import tqdm

from .config import Config
from .logger import weather_logger, monitor_data_freshness
from .models import DatabaseManager, WeatherObservation
from .weather_api import WeatherAPIClient, fetch_and_transform_location

class WeatherETLPipeline:
    """
    Main ETL pipeline for fetching, transforming, and loading weather data.
    """
    def __init__(self):
        self.config = Config
        self.logger = weather_logger
        self.db_manager = DatabaseManager(Config.get_database_url())
        self.api_client = WeatherAPIClient()
    
    def run_etl(self) -> bool:
        """
        Run the complete ETL pipeline for all configured locations.
        
        Returns:
            bool: True if successful, False otherwise
        """
        self.logger.info("Starting Weather ETL Pipeline")
        start_time = time.time()
        
        try:
            # Process all locations
            observations = self._process_locations()
            
            # Save all observations to database
            saved_count = self._save_observations(observations)
            
            # Optional: Push to S3
            if Config.PUSH_TO_S3 and Config.S3_BUCKET:
                self._push_to_s3(observations)
            
            end_time = time.time()
            self.logger.info(f"ETL Pipeline completed successfully. "
                           f"Processed {len(observations)} locations, saved {saved_count} records. "
                           f"Duration: {end_time - start_time:.2f} seconds")
            
            return True
        except Exception as e:
            self.logger.error(f"ETL Pipeline failed: {e}")
            return False
    
    def _process_locations(self) -> List[WeatherObservation]:
        """
        Process all configured locations and fetch weather data.
        
        Returns:
            List[WeatherObservation]: List of weather observations
        """
        observations = []
        
        self.logger.info(f"Processing {len(Config.LOCATIONS)} locations")
        
        # Use tqdm for progress bar
        for location in tqdm(Config.LOCATIONS, desc="Fetching weather data"):
            location = location.strip()
            if not location:
                continue
                
            try:
                observation = fetch_and_transform_location(location, self.api_client)
                if observation:
                    observations.append(observation)
            except Exception as e:
                self.logger.error(f"Failed to process location {location}: {e}")
                continue
        
        return observations
    
    def _save_observations(self, observations: List[WeatherObservation]) -> int:
        """
        Save weather observations to the database.
        
        Args:
            observations: List of weather observations to save
            
        Returns:
            int: Number of observations successfully saved
        """
        saved_count = 0
        
        self.logger.info(f"Saving {len(observations)} observations to database")
        
        for observation in observations:
            try:
                if self.db_manager.save_weather_observation(observation):
                    saved_count += 1
                else:
                    self.logger.warning(f"Failed to save observation for {observation.location}")
            except Exception as e:
                self.logger.error(f"Error saving observation for {observation.location}: {e}")
                continue
        
        self.logger.info(f"Successfully saved {saved_count}/{len(observations)} observations")
        return saved_count
    
    def _push_to_s3(self, observations: List[WeatherObservation]) -> bool:
        """
        Push raw weather data to S3 (if configured).
        
        Args:
            observations: List of weather observations to push
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not Config.S3_BUCKET:
            self.logger.warning("S3_BUCKET not configured. Skipping S3 push.")
            return False
            
        # Try to import boto3
        try:
            import boto3
            from botocore.exceptions import BotoCoreError, ClientError
        except ImportError:
            self.logger.error("boto3 not installed. Cannot push to S3.")
            return False
        
        self.logger.info(f"Pushing {len(observations)} raw JSON files to S3")
        
        try:
            s3_client = boto3.client("s3")
            pushed_count = 0
            
            for observation in observations:
                try:
                    # Create S3 key
                    key = f"weather_raw/{observation.location.replace(' ', '_')}/" \
                          f"{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}.json"
                    
                    # Push to S3
                    s3_client.put_object(
                        Bucket=Config.S3_BUCKET,
                        Key=key,
                        Body=observation.raw_json
                    )
                    
                    pushed_count += 1
                    self.logger.debug(f"Pushed raw JSON to s3://{Config.S3_BUCKET}/{key}")
                except (BotoCoreError, ClientError) as e:
                    self.logger.error(f"Failed to push to S3 for {observation.location}: {e}")
                    continue
                except Exception as e:
                    self.logger.error(f"Unexpected error pushing to S3 for {observation.location}: {e}")
                    continue
            
            self.logger.info(f"Successfully pushed {pushed_count}/{len(observations)} files to S3")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize S3 client: {e}")
            return False
    
    def health_check(self) -> dict:
        """
        Perform a health check on the pipeline.
        
        Returns:
            dict: Health report
        """
        self.logger.info("Performing health check")
        
        # Check data freshness
        freshness_report = monitor_data_freshness(self.db_manager)
        
        # Get latest observations
        latest_observations = self.db_manager.get_latest_observations(5)
        
        health_report = {
            "timestamp": datetime.utcnow().isoformat(),
            "freshness": freshness_report,
            "latest_observations": [
                obs.to_dict() for obs in latest_observations
            ]
        }
        
        return health_report

def run_pipeline() -> bool:
    """
    Run the weather ETL pipeline.
    
    Returns:
        bool: True if successful, False otherwise
    """
    pipeline = WeatherETLPipeline()
    return pipeline.run_etl()

def run_health_check() -> dict:
    """
    Run a health check on the pipeline.
    
    Returns:
        dict: Health report
    """
    pipeline = WeatherETLPipeline()
    return pipeline.health_check()