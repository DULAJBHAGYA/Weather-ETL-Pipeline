"""
Database initialization script for the Weather ETL Pipeline.
"""
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.config import Config
from src.models import DatabaseManager

def init_database():
    """Initialize the database and create tables."""
    print("Initializing database...")
    
    # Create necessary directories
    db_dir = os.path.dirname(Config.SQLITE_DB)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
        print(f"Created directory: {db_dir}")
    
    # Initialize database manager
    db_manager = DatabaseManager(Config.get_database_url())
    
    # Create tables
    print("Creating tables...")
    # The tables are created automatically when DatabaseManager is initialized
    
    print("Database initialization complete!")
    print(f"Database file: {Config.SQLITE_DB}")

if __name__ == "__main__":
    init_database()