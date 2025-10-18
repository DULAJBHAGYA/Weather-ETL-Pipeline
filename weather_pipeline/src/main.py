"""
Main entry point for the Weather ETL Pipeline.
"""
import argparse
import sys
from typing import Optional

from .config import Config
from .logger import weather_logger
from .pipeline import run_pipeline, run_health_check
from .scheduler import run_scheduler

def main():
    """
    Main entry point for the Weather ETL Pipeline.
    """
    parser = argparse.ArgumentParser(description="Weather ETL Pipeline")
    parser.add_argument(
        "command",
        choices=["run", "schedule", "health"],
        help="Command to execute: run (run once), schedule (run continuously), health (check health)"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=Config.SCHEDULE_INTERVAL_HOURS,
        help="Schedule interval in hours (default: 1)"
    )
    
    args = parser.parse_args()
    
    logger = weather_logger
    logger.info(f"Starting Weather ETL Pipeline with command: {args.command}")
    
    try:
        if args.command == "run":
            # Run the pipeline once
            success = run_pipeline()
            if success:
                logger.info("Pipeline completed successfully")
                return 0
            else:
                logger.error("Pipeline failed")
                return 1
                
        elif args.command == "schedule":
            # Run the scheduler
            logger.info(f"Starting scheduler with interval: {args.interval} hours")
            run_scheduler()
            return 0
            
        elif args.command == "health":
            # Run health check
            report = run_health_check()
            print(f"Health Check Report:")
            print(f"  Timestamp: {report['timestamp']}")
            print(f"  Freshness Issues: {len(report['freshness'].get('stale_locations', []))}")
            print(f"  Latest Observations: {len(report['latest_observations'])}")
            return 0
            
    except Exception as e:
        logger.error(f"Error executing command {args.command}: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())