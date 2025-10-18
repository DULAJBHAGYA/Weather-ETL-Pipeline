"""
Visualization module for the Weather ETL Pipeline.
"""
import pandas as pd
from typing import List, Optional
from datetime import datetime, timedelta

from .config import Config
from .logger import weather_logger
from .models import DatabaseManager, WeatherObservation

# Try to import visualization libraries
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    VISUALIZATION_AVAILABLE = True
except ImportError:
    plt = None
    sns = None
    VISUALIZATION_AVAILABLE = False

class WeatherVisualizer:
    """
    Visualizer for weather data.
    """
    def __init__(self):
        self.logger = weather_logger
        self.db_manager = DatabaseManager(Config.get_database_url())
        # Set up plotting style
        if VISUALIZATION_AVAILABLE and sns:
            sns.set_palette("husl")
    
    def plot_temperature_trends(self, days: int = 7, save_path: Optional[str] = None):
        """
        Plot temperature trends for the last N days.
        
        Args:
            days: Number of days to plot
            save_path: Path to save the plot (optional)
        """
        if not VISUALIZATION_AVAILABLE or not plt:
            self.logger.error("Visualization libraries not installed. Cannot generate plots.")
            return
            
        try:
            # Get data from database
            session = self.db_manager.get_session()
            try:
                # Calculate date threshold
                threshold_date = datetime.utcnow() - timedelta(days=days)
                
                # Query data
                observations = session.query(WeatherObservation).filter(
                    WeatherObservation.timestamp_utc >= threshold_date
                ).all()
                
                if not observations:
                    self.logger.warning("No data available for plotting")
                    return
                
                # Convert to DataFrame
                data = [obs.to_dict() for obs in observations]
                df = pd.DataFrame(data)
                
                # Convert timestamp to datetime
                df['timestamp_utc'] = pd.to_datetime(df['timestamp_utc'])
                
                # Create plot
                if plt:
                    plt.figure(figsize=(12, 8))
                
                # Plot temperature trends by location
                for location in df['location'].unique():
                    location_data = df[df['location'] == location]
                    if plt:
                        plt.plot(
                            location_data['timestamp_utc'], 
                            location_data['temp_c'], 
                            marker='o', 
                            label=location,
                            linewidth=2,
                            markersize=4
                        )
                
                if plt:
                    plt.title(f'Temperature Trends (Last {days} Days)', fontsize=16, pad=20)
                    plt.xlabel('Date/Time (UTC)', fontsize=12)
                    plt.ylabel('Temperature (°C)', fontsize=12)
                    plt.legend()
                    plt.grid(True, alpha=0.3)
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                
                # Save or show plot
                if save_path and plt:
                    plt.savefig(save_path, dpi=300, bbox_inches='tight')
                    self.logger.info(f"Temperature trends plot saved to {save_path}")
                elif plt:
                    plt.show()
                
                if plt:
                    plt.close()
                
            finally:
                session.close()
                
        except Exception as e:
            self.logger.error(f"Error plotting temperature trends: {e}")
            if plt:
                plt.close()
    
    def plot_humidity_distribution(self, days: int = 7, save_path: Optional[str] = None):
        """
        Plot humidity distribution for the last N days.
        
        Args:
            days: Number of days to plot
            save_path: Path to save the plot (optional)
        """
        if not VISUALIZATION_AVAILABLE or not plt:
            self.logger.error("Visualization libraries not installed. Cannot generate plots.")
            return
            
        try:
            # Get data from database
            session = self.db_manager.get_session()
            try:
                # Calculate date threshold
                threshold_date = datetime.utcnow() - timedelta(days=days)
                
                # Query data
                observations = session.query(WeatherObservation).filter(
                    WeatherObservation.timestamp_utc >= threshold_date
                ).all()
                
                if not observations:
                    self.logger.warning("No data available for plotting")
                    return
                
                # Convert to DataFrame
                data = [obs.to_dict() for obs in observations]
                df = pd.DataFrame(data)
                
                # Remove rows with missing humidity data
                df = df.dropna(subset=['humidity'])
                
                if df.empty:
                    self.logger.warning("No humidity data available for plotting")
                    return
                
                # Create plot
                if plt:
                    plt.figure(figsize=(10, 6))
                
                # Plot histogram
                if plt:
                    plt.hist(df['humidity'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
                    plt.title(f'Humidity Distribution (Last {days} Days)', fontsize=16, pad=20)
                    plt.xlabel('Humidity (%)', fontsize=12)
                    plt.ylabel('Frequency', fontsize=12)
                    plt.grid(True, alpha=0.3)
                    plt.tight_layout()
                
                # Save or show plot
                if save_path and plt:
                    plt.savefig(save_path, dpi=300, bbox_inches='tight')
                    self.logger.info(f"Humidity distribution plot saved to {save_path}")
                elif plt:
                    plt.show()
                
                if plt:
                    plt.close()
                
            finally:
                session.close()
                
        except Exception as e:
            self.logger.error(f"Error plotting humidity distribution: {e}")
            if plt:
                plt.close()
    
    def generate_summary_report(self) -> dict:
        """
        Generate a summary report of weather data.
        
        Returns:
            dict: Summary report
        """
        try:
            session = self.db_manager.get_session()
            try:
                # Get latest observations
                latest_observations = self.db_manager.get_latest_observations(10)
                
                # Get unique locations
                locations = session.query(WeatherObservation.location).distinct().all()
                locations = [loc[0] for loc in locations]
                
                # Get date range
                min_date = session.query(WeatherObservation.timestamp_utc).order_by(
                    WeatherObservation.timestamp_utc.asc()
                ).first()
                
                max_date = session.query(WeatherObservation.timestamp_utc).order_by(
                    WeatherObservation.timestamp_utc.desc()
                ).first()
                
                report = {
                    "total_observations": session.query(WeatherObservation).count(),
                    "unique_locations": len(locations),
                    "locations": locations,
                    "date_range": {
                        "start": min_date[0].isoformat() if min_date else None,
                        "end": max_date[0].isoformat() if max_date else None
                    },
                    "latest_observations": [
                        obs.to_dict() for obs in latest_observations
                    ]
                }
                
                return report
                
            finally:
                session.close()
                
        except Exception as e:
            self.logger.error(f"Error generating summary report: {e}")
            return {}

def generate_visualizations():
    """
    Generate standard visualizations.
    """
    if not VISUALIZATION_AVAILABLE:
        print("Visualization libraries not installed. Please install them with: pip install matplotlib seaborn")
        return {}
        
    visualizer = WeatherVisualizer()
    
    # Generate temperature trends
    visualizer.plot_temperature_trends(
        days=7, 
        save_path="./docs/temperature_trends.png"
    )
    
    # Generate humidity distribution
    visualizer.plot_humidity_distribution(
        days=7, 
        save_path="./docs/humidity_distribution.png"
    )
    
    # Generate summary report
    report = visualizer.generate_summary_report()
    
    return report

if __name__ == "__main__":
    generate_visualizations()