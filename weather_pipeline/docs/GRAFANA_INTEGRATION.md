# Grafana Integration Guide

This guide will help you set up Grafana to visualize your weather data from the SQLite database.

## Prerequisites

1. Grafana installed and running
2. SQLite database with weather data (populated by the ETL pipeline)
3. Grafana SQLite plugin installed

## Step 1: Access Grafana

1. Open your web browser and navigate to `http://localhost:3000`
2. Log in with the default credentials:
   - Username: `admin`
   - Password: `admin`
3. You'll be prompted to change the password - set it to something secure

## Step 2: Add SQLite Data Source

1. In the left sidebar, click the gear icon (Configuration) → **Data Sources**
2. Click **Add data source**
3. Search for "SQLite" and select it
4. Configure the data source:
   - **Name**: Weather Data
   - **Path**: [/Users/dulajupananda/Documents/Projects/Weather-ETL-Pipeline/weather_pipeline/db/weather.db](file:///Users/dulajupananda/Documents/Projects/Weather-ETL-Pipeline/weather_pipeline/db/weather.db)
   - (Adjust the path if your database is in a different location)
5. Click **Save & Test** - you should see a success message

## Step 3: Create Your First Dashboard

1. In the left sidebar, click the "+" icon → **Create** → **Dashboard**
2. Click **Add new panel**
3. In the query editor, enter this SQL query:
   ```sql
   SELECT 
     timestamp_utc as time,
     location,
     temp_c as temperature
   FROM weather_observations
   WHERE location = 'Colombo,Sri Lanka'
   ORDER BY timestamp_utc
   ```
4. Set the following options:
   - **Format** as "Time series"
   - **Time Column** as "time"
   - **Metric Column** as "temperature"
   - **Group By** as "location"
5. Click **Apply** in the top right

## Step 4: Add More Panels

### Temperature Trends Panel
1. Click **Add panel** → **Add new panel**
2. Use this query:
   ```sql
   SELECT 
     timestamp_utc as time,
     location,
     temp_c as temperature
   FROM weather_observations
   WHERE $__timeFilter(timestamp_utc)
   ORDER BY timestamp_utc
   ```
3. Set visualization to "Time series"
4. In the panel options, set title to "Temperature Trends"

### Current Weather Conditions
1. Click **Add panel** → **Add new panel**
2. Use this query:
   ```sql
   SELECT 
     location,
     temp_c as temperature,
     humidity,
     pressure,
     wind_speed
   FROM weather_observations
   WHERE timestamp_utc IN (
     SELECT MAX(timestamp_utc) 
     FROM weather_observations 
     GROUP BY location
   )
   ```
3. Set visualization to "Table"
4. Set title to "Current Weather Conditions"

### Humidity by Location
1. Click **Add panel** → **Add new panel**
2. Use this query:
   ```sql
   SELECT 
     timestamp_utc as time,
     location,
     humidity
   FROM weather_observations
   WHERE $__timeFilter(timestamp_utc)
   ORDER BY timestamp_utc
   ```
3. Set visualization to "Time series"
4. Set title to "Humidity Trends"

## Step 5: Configure Dashboard Variables

1. Go to **Dashboard settings** (gear icon in top right)
2. Click **Variables** → **Add variable**
3. Configure:
   - **Name**: location
   - **Type**: Query
   - **Data source**: Weather Data
   - **Query**: `SELECT DISTINCT location FROM weather_observations`
   - **Refresh**: On Dashboard Load
4. Click **Update**

Now you can use this variable in your queries by replacing hardcoded locations with `$location`

## Step 6: Sample Queries for Different Visualizations

### Average Temperature by Day
```sql
SELECT 
  date(timestamp_utc) as time,
  location,
  AVG(temp_c) as avg_temperature
FROM weather_observations
WHERE $__timeFilter(timestamp_utc)
GROUP BY date(timestamp_utc), location
ORDER BY time
```

### Wind Speed Gauge
```sql
SELECT 
  timestamp_utc as time,
  location,
  wind_speed
FROM weather_observations
WHERE location = '$location'
ORDER BY timestamp_utc DESC
LIMIT 1
```

### Pressure Trends
```sql
SELECT 
  timestamp_utc as time,
  location,
  pressure
FROM weather_observations
WHERE $__timeFilter(timestamp_utc) AND location = '$location'
ORDER BY timestamp_utc
```

## Step 7: Dashboard Layout Tips

1. **Organize panels logically** - Group related metrics together
2. **Use appropriate visualizations**:
   - Time series for trends over time
   - Gauges for current values
   - Tables for detailed data
   - Bar charts for comparisons
3. **Set appropriate time ranges** - Use the time picker in the top right
4. **Add annotations** - Mark special events or data quality issues

## Step 8: Set Up Auto-Refresh

1. Click the dropdown next to the time range selector in the top right
2. Select an auto-refresh interval (e.g., 5m for 5 minutes)
3. The dashboard will now automatically refresh with new data

## Troubleshooting

### Common Issues

1. **Data source connection failed**:
   - Check that the database path is correct
   - Ensure Grafana has read permissions on the database file
   - Verify the SQLite plugin is installed and loaded

2. **No data showing in panels**:
   - Check that your ETL pipeline has run and populated the database
   - Verify the time range in the dashboard matches your data
   - Check that your queries are correctly formatted

3. **Performance issues**:
   - Add database indexes on frequently queried columns
   - Limit the number of data points returned
   - Use $__timeFilter() in your queries to limit data by time range

### Useful SQLite Commands for Debugging

Check table structure:
```sql
.schema weather_observations
```

Count records:
```sql
SELECT COUNT(*) FROM weather_observations;
```

Check latest records:
```sql
SELECT * FROM weather_observations ORDER BY timestamp_utc DESC LIMIT 5;
```

## Next Steps

1. **Customize visualizations** - Experiment with different chart types
2. **Set up alerts** - Configure notifications for data quality issues
3. **Add more data sources** - Integrate other weather APIs or data
4. **Share dashboards** - Set up user accounts and permissions
5. **Automate deployment** - Use Grafana provisioning for consistent setups

Your weather dashboard is now ready to visualize real-time weather data as it's collected by your ETL pipeline!