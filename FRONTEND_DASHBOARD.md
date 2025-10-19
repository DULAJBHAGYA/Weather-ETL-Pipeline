# Weather Dashboard Frontend

A comprehensive Next.js dashboard for visualizing weather data using Chart.js.

## Overview

This frontend application provides a user-friendly interface to visualize weather data collected by the Weather ETL Pipeline. It features interactive charts, real-time data updates, and location-specific details.

## Features

- **Real-time Data Visualization**: Interactive charts for temperature, humidity, pressure, and wind speed
- **Location-based Views**: Detailed weather information for specific locations
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Auto-refresh**: Data updates every 5 minutes
- **TypeScript Support**: Type-safe codebase for reliability

## Technology Stack

- **Next.js 13+** with App Router
- **TypeScript** for type safety
- **Tailwind CSS** for styling
- **Chart.js** with **react-chartjs-2** for data visualization
- **SQLite** for data storage (via API routes)

## Project Structure

```
frontend/weather-dashboard/
├── src/
│   ├── app/                    # Next.js app directory
│   │   ├── api/               # API routes
│   │   │   └── weather/       # Weather data API endpoints
│   │   ├── location/          # Location-specific pages
│   │   ├── page.tsx           # Main dashboard page
│   │   └── layout.tsx         # Root layout
│   ├── components/            # React components
│   ├── lib/                   # Utility functions and types
│   └── styles/                # Global styles
├── public/                    # Static assets
└── package.json              # Project dependencies
```

## API Endpoints

- `GET /api/weather` - Get all weather data
- `GET /api/weather/latest` - Get latest weather data for each location
- `GET /api/weather/location/[location]` - Get weather data for a specific location

## Getting Started

### Prerequisites

1. Node.js 16.8 or later
2. npm, yarn, or pnpm
3. The Weather ETL Pipeline backend running with data in the SQLite database

### Installation

1. Navigate to the frontend directory:
   ```bash
   cd /Users/dulajupananda/Documents/Projects/Weather-ETL-Pipeline/frontend/weather-dashboard
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

### Development

1. Start the development server:
   ```bash
   npm run dev
   ```

2. Open [http://localhost:3000](http://localhost:3000) in your browser

### Production

1. Build the application:
   ```bash
   npm run build
   ```

2. Start the production server:
   ```bash
   npm start
   ```

## Dashboard Components

### 1. Main Dashboard (`/`)

Displays:
- Current conditions cards for all locations
- Temperature trends chart
- Humidity trends chart

### 2. Location Details (`/location/[location]`)

Displays:
- Latest weather conditions for the specific location
- Temperature trends chart
- Humidity trends chart
- Pressure trends chart
- Wind speed trends chart

## Data Visualization

The dashboard includes several chart types:

1. **Temperature Trends** - Line chart showing temperature changes over time
2. **Humidity Trends** - Line chart showing humidity changes over time
3. **Pressure Trends** - Line chart showing atmospheric pressure changes
4. **Wind Speed Trends** - Line chart showing wind speed changes

## Customization

You can customize the dashboard by:

1. Adding new chart types in `src/lib/chartUtils.ts`
2. Creating new API endpoints in `src/app/api/`
3. Adding new pages in `src/app/`
4. Modifying the styling in `src/app/globals.css`

## Troubleshooting

### Database Connection Issues

Make sure the SQLite database file exists at:
```
/Users/dulajupananda/Documents/Projects/Weather-ETL-Pipeline/weather_pipeline/db/weather.db
```

### API Route Errors

Check that the API routes in `src/app/api/weather/` are correctly configured and have proper error handling.

### Port Conflicts

If port 3000 is in use by another application:
```bash
# Kill the process using port 3000
lsof -i :3000
kill -9 <PID>

# Or run on a different port
PORT=3001 npm run dev
```

## Integration with Weather ETL Pipeline

The frontend integrates seamlessly with the existing Weather ETL Pipeline:

1. Reads data from the same SQLite database
2. Automatically updates when the pipeline collects new data
3. Provides visualization for all data collected by the pipeline

## Future Enhancements

1. **User Authentication** - Add login functionality for personalized dashboards
2. **Alerts System** - Email or SMS notifications for extreme weather conditions
3. **Historical Data Analysis** - Advanced analytics and trend predictions
4. **Map Integration** - Geographical visualization of weather data
5. **Export Functionality** - Export data as CSV or PDF reports

## Learn More

To learn more about the technologies used:

- [Next.js Documentation](https://nextjs.org/docs)
- [Chart.js Documentation](https://www.chartjs.org/docs/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)