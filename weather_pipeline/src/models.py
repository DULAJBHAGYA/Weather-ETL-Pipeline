"""
Database models for the Weather ETL Pipeline.
"""
from sqlalchemy import (
    create_engine, 
    Column, 
    Integer, 
    String, 
    Float, 
    DateTime, 
    Text,
    Index,
    func
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime
from typing import Optional

Base = declarative_base()

class WeatherObservation(Base):
    """
    Model representing a weather observation record.
    """
    __tablename__ = 'weather_observations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    location = Column(String, nullable=False)
    lat = Column(Float)
    lon = Column(Float)
    timestamp_utc = Column(DateTime, nullable=False)
    temp_c = Column(Float)
    temp_k = Column(Float)
    feels_like_c = Column(Float)
    humidity = Column(Integer)
    pressure = Column(Integer)
    wind_speed = Column(Float)
    wind_deg = Column(Integer)
    weather_main = Column(String)
    weather_description = Column(String)
    raw_json = Column(Text)
    fetched_at_utc = Column(DateTime, nullable=False, default=func.current_timestamp())
    
    # Index for faster queries
    __table_args__ = (
        Index('idx_location_timestamp', 'location', 'timestamp_utc'),
        Index('idx_fetched_at', 'fetched_at_utc'),
    )
    
    def __repr__(self):
        return f"<WeatherObservation(location='{self.location}', timestamp='{self.timestamp_utc}', temp_c={self.temp_c})>"
    
    def to_dict(self):
        """Convert the model instance to a dictionary."""
        return {
            'id': self.id,
            'location': self.location,
            'lat': self.lat,
            'lon': self.lon,
            'timestamp_utc': self.timestamp_utc.isoformat() if self.timestamp_utc is not None else None,
            'temp_c': self.temp_c,
            'temp_k': self.temp_k,
            'feels_like_c': self.feels_like_c,
            'humidity': self.humidity,
            'pressure': self.pressure,
            'wind_speed': self.wind_speed,
            'wind_deg': self.wind_deg,
            'weather_main': self.weather_main,
            'weather_description': self.weather_description,
            'raw_json': self.raw_json,
            'fetched_at_utc': self.fetched_at_utc.isoformat() if self.fetched_at_utc is not None else None
        }

class DatabaseManager:
    """
    Manager class for database operations.
    """
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url, echo=False, connect_args={"check_same_thread": False})
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self._create_tables()
    
    def _create_tables(self):
        """Create all tables defined in the models."""
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self):
        """Get a database session."""
        return self.SessionLocal()
    
    def save_weather_observation(self, observation: WeatherObservation) -> bool:
        """
        Save a weather observation to the database.
        
        Args:
            observation: WeatherObservation instance to save
            
        Returns:
            bool: True if successful, False otherwise
        """
        session = self.get_session()
        try:
            session.add(observation)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error saving observation: {e}")
            return False
        finally:
            session.close()
    
    def get_latest_observations(self, limit: int = 10) -> list:
        """
        Get the latest weather observations.
        
        Args:
            limit: Number of records to return
            
        Returns:
            list: List of WeatherObservation instances
        """
        session = self.get_session()
        try:
            return session.query(WeatherObservation).order_by(
                WeatherObservation.fetched_at_utc.desc()
            ).limit(limit).all()
        finally:
            session.close()
    
    def get_stale_locations(self, minutes_threshold: int = 90) -> list:
        """
        Get locations with stale data based on the threshold.
        
        Args:
            minutes_threshold: Threshold in minutes to consider data stale
            
        Returns:
            list: List of locations with stale data
        """
        session = self.get_session()
        try:
            # This is a simplified query - in a real implementation, you might want to use
            # a more complex query to get the latest timestamp per location
            from sqlalchemy import text
            result = session.execute(text("""
                SELECT location, MAX(fetched_at_utc) as latest_fetch
                FROM weather_observations 
                GROUP BY location
                HAVING MAX(fetched_at_utc) < datetime('now', '-{} minutes')
            """.format(minutes_threshold)))
            return list(result.fetchall())
        finally:
            session.close()
