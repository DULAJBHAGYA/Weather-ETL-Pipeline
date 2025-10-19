"""
Scheduler for the Weather ETL Pipeline.
"""
import time
import threading
from datetime import datetime
from typing import Callable, Optional

from .config import Config
from .logger import weather_logger
from .pipeline import run_pipeline

# Conditional import for schedule
try:
    import schedule
    SCHEDULE_AVAILABLE = True
except ImportError:
    schedule = None
    SCHEDULE_AVAILABLE = False

class WeatherScheduler:
    """
    Scheduler for running the weather ETL pipeline at regular intervals.
    """
    def __init__(self):
        self.logger = weather_logger
        self.interval_hours = Config.SCHEDULE_INTERVAL_HOURS
        self._running = False
        self._thread: Optional[threading.Thread] = None
    
    def start_scheduler(self):
        """
        Start the scheduler to run the ETL pipeline at regular intervals.
        """
        if not SCHEDULE_AVAILABLE:
            self.logger.error("Schedule library not installed. Cannot start scheduler.")
            return
            
        if self._running:
            self.logger.warning("Scheduler is already running")
            return
        
        self._running = True
        
        # Schedule the job based on interval (supporting fractional hours)
        if schedule:
            if self.interval_hours >= 1:
                schedule.every(int(self.interval_hours)).hours.do(self._run_etl_job)
            else:
                # Convert to minutes for intervals less than 1 hour
                minutes = int(self.interval_hours * 60)
                schedule.every(minutes).minutes.do(self._run_etl_job)
        
        # Run the scheduler in a separate thread
        self._thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self._thread.start()
        
        # Calculate interval in minutes for logging
        interval_minutes = int(self.interval_hours * 60)
        self.logger.info(f"Scheduler started. ETL pipeline will run every {interval_minutes} minute(s)")
    
    def stop_scheduler(self):
        """
        Stop the scheduler.
        """
        if not SCHEDULE_AVAILABLE or not schedule:
            return
            
        if not self._running:
            self.logger.warning("Scheduler is not running")
            return
        
        self._running = False
        if schedule:
            schedule.clear()
        
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=5)
        
        self.logger.info("Scheduler stopped")
    
    def run_once(self):
        """
        Run the ETL pipeline once.
        """
        self.logger.info("Running ETL pipeline once")
        return run_pipeline()
    
    def _run_etl_job(self):
        """
        Run the ETL job.
        """
        try:
            self.logger.info("Starting scheduled ETL job")
            success = run_pipeline()
            if success:
                self.logger.info("Scheduled ETL job completed successfully")
            else:
                self.logger.error("Scheduled ETL job failed")
        except Exception as e:
            self.logger.error(f"Error in scheduled ETL job: {e}")
    
    def _run_scheduler(self):
        """
        Run the scheduler loop.
        """
        if not SCHEDULE_AVAILABLE or not schedule:
            return
            
        while self._running:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except KeyboardInterrupt:
                self.logger.info("Scheduler interrupted by user")
                self.stop_scheduler()
                break
            except Exception as e:
                self.logger.error(f"Error in scheduler loop: {e}")
                time.sleep(60)  # Continue running even if there's an error

def run_scheduler():
    """
    Run the weather ETL pipeline scheduler.
    """
    if not SCHEDULE_AVAILABLE:
        print("Schedule library not installed. Please install it with: pip install schedule")
        return
        
    scheduler = WeatherScheduler()
    
    try:
        scheduler.start_scheduler()
        
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Scheduler interrupted by user")
        scheduler.stop_scheduler()

if __name__ == "__main__":
    run_scheduler()