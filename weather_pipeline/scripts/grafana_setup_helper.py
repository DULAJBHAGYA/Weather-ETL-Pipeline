"""
Helper script for setting up Grafana with the weather data.
"""
import os
import subprocess
import sys
import time

def check_grafana_status():
    """Check if Grafana is running."""
    try:
        result = subprocess.run(['brew', 'services', 'list'], 
                              capture_output=True, text=True)
        if 'grafana' in result.stdout and 'started' in result.stdout:
            print("✓ Grafana is running")
            return True
        else:
            print("✗ Grafana is not running")
            return False
    except Exception as e:
        print(f"Error checking Grafana status: {e}")
        return False

def start_grafana():
    """Start Grafana service."""
    try:
        subprocess.run(['brew', 'services', 'start', 'grafana'], 
                      check=True, capture_output=True)
        print("✓ Grafana started successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error starting Grafana: {e}")
        return False

def install_sqlite_plugin():
    """Install SQLite plugin for Grafana."""
    try:
        # Try to install the plugin
        result = subprocess.run([
            '/opt/homebrew/bin/grafana', 'cli',
            '--homepath', '/opt/homebrew/opt/grafana/share/grafana',
            '--pluginsDir', '/opt/homebrew/var/lib/grafana/plugins',
            'plugins', 'install', 'frser-sqlite-datasource'
        ], check=True, capture_output=True, text=True)
        
        print("✓ SQLite plugin installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing SQLite plugin: {e}")
        print("You may need to install it manually with:")
        print("sudo /opt/homebrew/bin/grafana cli --homepath /opt/homebrew/opt/grafana/share/grafana --pluginsDir /opt/homebrew/var/lib/grafana/plugins plugins install frser-sqlite-datasource")
        return False

def restart_grafana():
    """Restart Grafana to load plugins."""
    try:
        subprocess.run(['brew', 'services', 'restart', 'grafana'], 
                      check=True, capture_output=True)
        print("✓ Grafana restarted successfully")
        # Wait a moment for Grafana to fully start
        time.sleep(5)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error restarting Grafana: {e}")
        return False

def check_database_exists():
    """Check if the weather database exists and has data."""
    db_path = "./db/weather.db"
    if not os.path.exists(db_path):
        print("✗ Database file not found")
        return False
    
    try:
        import sqlite3
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM weather_observations")
        count = cursor.fetchone()[0]
        conn.close()
        
        if count > 0:
            print(f"✓ Database found with {count} records")
            return True
        else:
            print("⚠ Database exists but is empty")
            return True
    except Exception as e:
        print(f"Error checking database: {e}")
        return False

def get_database_path():
    """Get the absolute path to the database."""
    return os.path.abspath("./db/weather.db")

def main():
    """Main setup helper function."""
    print("Grafana Setup Helper for Weather ETL Pipeline")
    print("=" * 50)
    
    # Check if database exists
    print("\n1. Checking database...")
    if not check_database_exists():
        print("Please run the ETL pipeline or populate_sample_data.py first")
        return 1
    
    # Check Grafana status
    print("\n2. Checking Grafana status...")
    if not check_grafana_status():
        print("Starting Grafana...")
        if not start_grafana():
            return 1
    
    # Check if plugin is installed
    print("\n3. Checking SQLite plugin...")
    # This is a simplified check - in reality, you'd want to check if the plugin
    # directory exists and contains the plugin files
    plugin_path = "/opt/homebrew/var/lib/grafana/plugins/frser-sqlite-datasource"
    if not os.path.exists(plugin_path):
        print("Installing SQLite plugin...")
        if not install_sqlite_plugin():
            return 1
        
        print("Restarting Grafana to load plugin...")
        if not restart_grafana():
            return 1
    
    # Print setup instructions
    print("\n4. Setup Instructions")
    print("-" * 20)
    print("1. Open your browser and go to: http://localhost:3000")
    print("2. Log in with username 'admin' and password 'admin'")
    print("3. Change your password when prompted")
    print("4. Go to Configuration → Data Sources → Add data source")
    print("5. Select SQLite")
    print(f"6. Set Path to: {get_database_path()}")
    print("7. Set Name to: Weather Data")
    print("8. Click Save & Test")
    print("9. Create a new dashboard and add panels using the sample queries")
    print("   from the GRAFANA_INTEGRATION.md documentation")
    
    print("\n✓ Setup helper completed successfully!")
    return 0

if __name__ == "__main__":
    sys.exit(main())