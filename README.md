# Weather ETL Pipeline

A robust, scalable weather data pipeline that fetches current weather data from OpenWeatherMap API, processes and stores it in SQLite, and provides visualization capabilities.

## Project Structure

The project is organized as follows:

```
.
├── weather_pipeline/           # Main pipeline implementation
│   ├── src/                   # Source code
│   ├── tests/                 # Unit tests
│   ├── db/                    # SQLite database files
│   ├── logs/                  # Log files
│   ├── docs/                  # Documentation and visualizations
│   ├── scripts/               # Setup and utility scripts
│   ├── docker/                # Docker configuration
│   ├── requirements.txt       # Python dependencies
│   ├── .env.template         # Environment variables template
│   └── README.md             # Detailed pipeline documentation
└── README.md                 # This file
```

## Quick Start

1. Navigate to the weather_pipeline directory:
   ```bash
   cd weather_pipeline
   ```

2. Run the setup script:
   ```bash
   ./scripts/setup.sh
   ```

3. Edit the `.env` file to add your OpenWeatherMap API key:
   ```bash
   # Copy the template and edit it
   cp .env.template .env
   # Edit .env with your API key and configurations
   ```

4. Run the pipeline:
   ```bash
   python -m src.main run
   ```

## Features

- **Data Extraction**: Fetches current weather data from OpenWeatherMap API
- **Data Transformation**: Cleans and transforms raw weather data
- **Data Loading**: Stores processed data in SQLite database
- **Scheduling**: Runs automatically at configurable intervals
- **Monitoring**: Built-in logging and health checks
- **Visualization**: Generates charts and reports
- **Error Handling**: Retry mechanisms and graceful failure handling
- **Containerization**: Docker support for easy deployment

## Documentation

For detailed documentation, see [weather_pipeline/README.md](weather_pipeline/README.md).