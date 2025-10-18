"""
Database test script for the Weather ETL Pipeline.
"""
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.config import Config
from src.models import DatabaseManager, WeatherObservation

def test_database():
    """Test database connection and basic operations."""
    print("Testing database connection...")
    
    try:
        # Initialize database manager
        db_manager = DatabaseManager(Config.get_database_url())
        
        # Test connection by getting a session
        session = db_manager.get_session()
        session.close()
        
        print("Database connection successful!")
        
        # Test table creation by checking if we can query
        session = db_manager.get_session()
        try:
            count = session.query(WeatherObservation).count()
            print(f"Database contains {count} weather observations")
        except Exception as e:
            print(f"Table may not exist yet or is empty: {e}")
        finally:
            session.close()
            
        return True
        
    except Exception as e:
        print(f"Database test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_database()
    sys.exit(0 if success else 1)