# Weather ETL Pipeline

A robust, scalable weather data pipeline that fetches current weather data from OpenWeatherMap API, processes and stores it in SQLite, and provides visualization capabilities.

## Features

- **Data Extraction**: Fetches current weather data from OpenWeatherMap API
- **Data Transformation**: Cleans and transforms raw weather data
- **Data Loading**: Stores processed data in SQLite database
- **Scheduling**: Runs automatically at configurable intervals
- **Monitoring**: Built-in logging and health checks
- **Visualization**: Generates charts and reports
- **Error Handling**: Retry mechanisms and graceful failure handling
- **Scalability**: Modular architecture for easy extension

## Project Structure

```
weather_pipeline/
├── src/                    # Source code
│   ├── config.py          # Configuration management
│   ├── models.py          # Database models
│   ├── logger.py          # Logging utilities
│   ├── weather_api.py     # Weather API client
│   ├── pipeline.py        # Main ETL pipeline
│   ├── scheduler.py        # Scheduling functionality
│   ├── visualization.py   # Data visualization
│   └── main.py            # Main entry point
├── tests/                 # Unit tests
├── db/                    # SQLite database files
├── logs/                  # Log files
├── docs/                  # Documentation and visualizations
├── requirements.txt       # Python dependencies
├── .env.template         # Environment variables template
└── README.md             # This file
```

## Prerequisites

- Python 3.8+
- pip
- OpenWeatherMap API key (sign up at [openweathermap.org](https://openweathermap.org/api))
- SQLite3 (usually comes pre-installed with Python)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd weather-pipeline
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r weather_pipeline/requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp weather_pipeline/.env.template weather_pipeline/.env
   ```
   Edit `weather_pipeline/.env` and add your OpenWeatherMap API key and other configurations.

## Configuration

Create a `.env` file based on `.env.template` with the following variables:

```env
# OpenWeather API Configuration
OWM_API_KEY=your_openweather_api_key_here

# Locations to fetch weather data for (semicolon-separated)
# Format: "City,Country" or "lat,lon"
LOCATIONS=Colombo,Sri Lanka;London,UK;New York,US

# Database Configuration
SQLITE_DB=./db/weather.db

# S3 Configuration (optional)
S3_BUCKET=your-bucket-name
PUSH_TO_S3=false

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=./logs/pipeline.log

# Scheduler Configuration
SCHEDULE_INTERVAL_HOURS=1

# Retry Configuration
MAX_RETRIES=3
RETRY_DELAY_SECONDS=5

# Data Validation
MIN_TEMP_C=-100
MAX_TEMP_C=100
```

## Usage

### Run Once

To run the pipeline once:

```bash
python -m src.main run
```

### Run Continuously (Scheduled)

To run the pipeline continuously with the configured schedule:

```bash
python -m src.main schedule
```

### Health Check

To run a health check:

```bash
python -m src.main health
```

### Generate Visualizations

To generate visualizations:

```bash
python -m src.visualization
```

## Database Schema

The pipeline uses a SQLite database with the following schema:

```sql
CREATE TABLE weather_observations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  location TEXT NOT NULL,
  lat REAL,
  lon REAL,
  timestamp_utc TEXT NOT NULL,
  temp_c REAL,
  temp_k REAL,
  feels_like_c REAL,
  humidity INTEGER,
  pressure INTEGER,
  wind_speed REAL,
  wind_deg INTEGER,
  weather_main TEXT,
  weather_description TEXT,
  raw_json TEXT,
  fetched_at_utc TEXT NOT NULL
);

CREATE INDEX idx_location_timestamp ON weather_observations(location, timestamp_utc);
CREATE INDEX idx_fetched_at ON weather_observations(fetched_at_utc);
```

## Monitoring

The pipeline includes built-in monitoring capabilities:

- **Logging**: All operations are logged to the configured log file
- **Health Checks**: Monitor data freshness and system status
- **Error Handling**: Automatic retries with exponential backoff

## Testing

Run unit tests with pytest:

```bash
pytest tests/
```

## Extending the Pipeline

The modular architecture makes it easy to extend the pipeline:

1. **Add new data sources**: Implement new API clients in `src/`
2. **Add new transformations**: Extend the transformation logic in `src/weather_api.py`
3. **Add new visualizations**: Add new methods to `src/visualization.py`
4. **Add new storage backends**: Extend the database manager in `src/models.py`

## Performance Considerations

- **Batch Processing**: The pipeline processes multiple locations in batches
- **Connection Pooling**: Database connections are efficiently managed
- **Memory Management**: Data is processed in chunks to minimize memory usage
- **Caching**: API responses can be cached to reduce load

## Troubleshooting

### Common Issues

1. **API Key Error**: Ensure your OpenWeatherMap API key is correctly set in `.env`
2. **Database Permissions**: Ensure the application has write permissions to the database directory
3. **Network Issues**: Check your internet connection and firewall settings

### Logs

Check the log file specified in `LOG_FILE` for detailed error information.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.