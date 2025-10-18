"""
Script to test database connection and retrieve sample data.
"""
import sqlite3
import os

def test_database_connection():
    """Test connection to the SQLite database and retrieve sample data."""
    db_path = "./db/weather.db"
    
    if not os.path.exists(db_path):
        print(f"Database file not found at {db_path}")
        return False
    
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get table info
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("Tables in database:")
        for table in tables:
            print(f"  - {table[0]}")
        
        # Get row count
        cursor.execute("SELECT COUNT(*) FROM weather_observations")
        count = cursor.fetchone()[0]
        print(f"\nTotal records in weather_observations: {count}")
        
        # Get sample data
        cursor.execute("""
            SELECT location, timestamp_utc, temp_c, humidity, pressure 
            FROM weather_observations 
            LIMIT 5
        """)
        rows = cursor.fetchall()
        
        print("\nSample data:")
        print("Location | Timestamp | Temperature (°C) | Humidity (%) | Pressure (hPa)")
        print("-" * 70)
        for row in rows:
            print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]}")
        
        # Get unique locations
        cursor.execute("SELECT DISTINCT location FROM weather_observations")
        locations = cursor.fetchall()
        print(f"\nLocations in database:")
        for location in locations:
            print(f"  - {location[0]}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return False

if __name__ == "__main__":
    test_database_connection()