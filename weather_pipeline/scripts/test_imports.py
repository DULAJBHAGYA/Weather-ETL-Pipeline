"""
Test script to verify imports work correctly.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_models_import():
    """Test importing models module."""
    try:
        from src.models import WeatherObservation, DatabaseManager
        print("✓ models module imported successfully")
        return True
    except Exception as e:
        print(f"✗ models module import failed: {e}")
        return False

def test_config_import():
    """Test importing config module."""
    try:
        from src.config import Config
        print("✓ config module imported successfully")
        return True
    except Exception as e:
        print(f"✗ config module import failed: {e}")
        return False

def test_logger_import():
    """Test importing logger module."""
    try:
        from src.logger import WeatherLogger, weather_logger
        print("✓ logger module imported successfully")
        return True
    except Exception as e:
        print(f"✗ logger module import failed: {e}")
        return False

def test_weather_api_import():
    """Test importing weather_api module."""
    try:
        from src.weather_api import WeatherAPIClient, WeatherAPIError
        print("✓ weather_api module imported successfully")
        return True
    except Exception as e:
        print(f"✗ weather_api module import failed: {e}")
        return False

def test_pipeline_import():
    """Test importing pipeline module."""
    try:
        from src.pipeline import WeatherETLPipeline
        print("✓ pipeline module imported successfully")
        return True
    except Exception as e:
        print(f"✗ pipeline module import failed: {e}")
        return False

def test_scheduler_import():
    """Test importing scheduler module."""
    try:
        from src.scheduler import WeatherScheduler
        print("✓ scheduler module imported successfully")
        return True
    except Exception as e:
        print(f"✗ scheduler module import failed: {e}")
        return False

def test_visualization_import():
    """Test importing visualization module."""
    try:
        from src.visualization import WeatherVisualizer
        print("✓ visualization module imported successfully")
        return True
    except Exception as e:
        print(f"✗ visualization module import failed: {e}")
        return False

def main():
    """Run all import tests."""
    print("Testing module imports...")
    print("=" * 30)
    
    tests = [
        test_models_import,
        test_config_import,
        test_logger_import,
        test_weather_api_import,
        test_pipeline_import,
        test_scheduler_import,
        test_visualization_import
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("=" * 30)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("All imports successful!")
        return 0
    else:
        print("Some imports failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())