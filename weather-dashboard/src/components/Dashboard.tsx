import React, { useState, useEffect, useRef, useCallback } from 'react';
import { mockLocationData } from '../mockData';
import kandyImage from '../assets/kandy.png';
import colomboImage from '../assets/colombo.png';
import anuradhapuraImage from '../assets/anuradhapura.png';
import { MdLocationOn, MdWaterDrop, MdSync } from "react-icons/md";
import { RiTempColdFill } from "react-icons/ri";
import { FaWind } from "react-icons/fa";

interface WeatherData {
  id: number;
  location: string;
  temperature_celsius: number;
  feels_like_celsius: number;
  humidity_percent: number;
  wind_speed_ms: number;
  pressure_hpa: number;
  visibility_meters: number;
  weather_main: string;
  weather_description: string;
  timestamp: string;
}

const Dashboard: React.FC = () => {
  // State for weather data
  const [weatherData, setWeatherData] = useState<WeatherData[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<string>('');
  const [isRefreshing, setIsRefreshing] = useState<boolean>(false);
  
  // Store the latest data IDs to detect changes
  const latestDataIds = useRef<{[key: string]: number}>({});

  // Fetch weather data from the backend API
  const fetchWeatherData = useCallback(async () => {
    try {
      setIsRefreshing(true);
      // Try to fetch from our Python API server
      const response = await fetch('http://localhost:8000/api/weather/latest');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data: WeatherData[] = await response.json();
      
      // Check if data has actually changed
      const newDataIds: {[key: string]: number} = {};
      let hasChanged = false;
      
      data.forEach(location => {
        newDataIds[location.location] = location.id;
        if (latestDataIds.current[location.location] !== location.id) {
          hasChanged = true;
        }
      });
      
      // Only update state if data has changed or it's the first load
      if (hasChanged || weatherData.length === 0) {
        // Filter to only show Kandy, Colombo, and Anuradhapura (should already be filtered by API)
        const filteredData = data.filter((location: WeatherData) => 
          ['Kandy', 'Colombo', 'Anuradhapura'].includes(location.location)
        );
        
        setWeatherData(filteredData);
        latestDataIds.current = newDataIds;
        // Set last updated time in Sri Lanka timezone
        const now = new Date();
        setLastUpdated(now.toLocaleTimeString([], { 
          hour: '2-digit', 
          minute: '2-digit',
          timeZone: 'Asia/Colombo'
        }));
        setError(null);
      }
    } catch (err) {
      console.error('Error fetching weather data:', err);
      setError('Failed to fetch weather data. Using mock data instead.');
      // Fallback to mock data if API fails
      setWeatherData(mockLocationData.map(loc => loc.latest));
    } finally {
      setLoading(false);
      setIsRefreshing(false);
    }
  }, [weatherData.length]);

  useEffect(() => {
    fetchWeatherData();
    
    // Set up polling to refresh data every 1 minute (increased frequency)
    const intervalId = setInterval(fetchWeatherData, 60 * 1000);
    
    // Clean up interval on component unmount
    return () => clearInterval(intervalId);
  }, [fetchWeatherData]);

  const getWeatherIcon = (weatherMain: string) => {
    switch (weatherMain.toLowerCase()) {
      case 'clear':
        return <img src="/assets/day.svg" alt="Clear" className="w-20 h-20 md:w-36 md:h-36" />;
      case 'clouds':
        return <img src="/assets/cloudy.svg" alt="Cloudy" className="w-20 h-20 md:w-36 md:h-36" />;
      case 'rain':
        return <img src="/assets/rain.svg" alt="Rain" className="w-20 h-20 md:w-36 md:h-36" />;
      case 'night':
        return <img src="/assets/night.svg" alt="Night" className="w-20 h-20 md:w-36 md:h-36" />;
      case 'snow':
        return <img src="/assets/snowy.svg" alt="Snow" className="w-20 h-20 md:w-36 md:h-36" />;
      case 'thunderstorm':
        return <img src="/assets/thunder.svg" alt="Thunderstorm" className="w-20 h-20 md:w-36 md:h-36" />;
      default:
        return <img src="/assets/default.svg" alt="Default" className="w-20 h-20 md:w-36 md:h-36" />;
    }
  };

  const formatTime = (timestamp: string) => {
    // Convert UTC timestamp to local time (Sri Lanka is UTC+5:30)
    const date = new Date(timestamp);
    // For Sri Lanka, we add 5 hours and 30 minutes to UTC
    return date.toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit',
      timeZone: 'Asia/Colombo'
    });
  };

  const getKPIIcon = (kpiname: string): React.ReactElement | null => {
    switch (kpiname) {
        case 'location':
      return <MdLocationOn className="w-8 h-8 text-gray-600" />;
        case 'temp':
      return <RiTempColdFill className="w-8 h-8 text-gray-600" />;
        case 'humidity':
      return <MdWaterDrop className="w-8 h-8 text-gray-600" />;
        case 'wind':
      return <FaWind className="w-8 h-8 text-gray-600" />;
        default:
            return null;
    }
  };

  // Get current date and time in Sri Lanka timezone
  const getCurrentDateTime = () => {
    const now = new Date();
    return now.toLocaleString([], { 
      weekday: 'long', 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric',
      hour: '2-digit', 
      minute: '2-digit',
      timeZone: 'Asia/Colombo'
    });
  };

  // Filter to only show Kandy, Colombo, and Anuradhapura (for mock data fallback)
  const filteredLocationData = mockLocationData.filter(location => 
    ['Kandy', 'Colombo', 'Anuradhapura'].includes(location.location)
  );

  // Use API data if available, otherwise fallback to mock data
  const displayData = weatherData.length > 0 ? weatherData : filteredLocationData.map(loc => loc.latest);

  // Function to get the appropriate image for each location
  const getLocationImage = (location: string): string | undefined => {
    switch (location) {
      case 'Kandy':
        return kandyImage;
      case 'Colombo':
        return colomboImage;
      case 'Anuradhapura':
        return anuradhapuraImage;
      default:
        return undefined;
    }
  };

  return (
    <div className="min-h-screen relative p-2 py-16 md:py-16 flex flex-col">
      {/* Background image with overlay */}
      <div className="absolute inset-0 z-0">
        <img 
          src="/assets/background.jpg" 
          alt="Weather Background" 
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-blue-50 bg-opacity-70"></div>
      </div>

      <div className="relative z-10 mx-auto w-[90%] flex-grow flex flex-col">
        {/* Header */}
        <header className="mb-6 md:mb-8 text-left">
          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-3xl md:text-3xl lg:text-4xl font-extrabold text-black mb-2">TROPICAST Weather Dashboard</h1>
              <p className="text-black font-semibold text-lg md:text-lg">Real-time weather monitoring for Kandy, Colombo, and Anuradhapura</p>
              {/* Current date and time - same style as above text */}
              <p className="text-black font-semibold text-lg md:text-lg">{getCurrentDateTime()}</p>
            </div>
            <button 
              onClick={fetchWeatherData}
              disabled={isRefreshing}
              className={`p-2 rounded-full ${isRefreshing ? 'bg-gray-300' : 'bg-blue-100 hover:bg-blue-200'} transition-colors`}
              title="Refresh data"
            >
              <MdSync className={`w-6 h-6 text-blue-600 ${isRefreshing ? 'animate-spin' : ''}`} />
            </button>
          </div>
          {loading && <p className="text-black font-semibold text-lg md:text-lg">Loading weather data...</p>}
          {error && <p className="text-red-500 font-semibold text-lg md:text-lg">{error}</p>}
          {lastUpdated && !loading && (
            <p className="text-green-600 font-semibold text-lg md:text-lg">
              Last updated: {lastUpdated} {isRefreshing && "(Refreshing...)"}
            </p>
          )}
        </header>

        {/* Stats Overview */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6 md:mb-8">
          <div className="p-8 rounded-3xl shadow-lg h-32 md:h-32 lg:h-32">
            <div className="flex items-center">
              <div className="p-6 bg-white/50 rounded-3xl">
                {getKPIIcon('location')}
              </div>
              <div className="ml-4">
                <p className="text-lg font-medium text-gray-600">Locations Tracked</p>
                <p className="text-2xl md:text-3xl font-bold text-black">{filteredLocationData.length}</p>
              </div>
            </div>
          </div>

          <div className=" p-6 rounded-3xl shadow-lg h-32 md:h-32 lg:h-32">
            <div className="flex items-center">
              <div className="p-6 bg-white/50 rounded-3xl">
                {getKPIIcon('temp')}
              </div>
              <div className="ml-4">
                <p className="text-lg font-medium text-gray-600">Avg Temperature</p>
                <p className="text-2xl md:text-3xl font-bold text-black">
                  {Math.round(filteredLocationData.reduce((sum, loc) => sum + loc.latest.temperature_celsius, 0) / filteredLocationData.length)}°C
                </p>
              </div>
            </div>
          </div>

          <div className=" p-6 rounded-3xl shadow-lg h-32 md:h-32 lg:h-32">
            <div className="flex items-center">
              <div className="p-6 bg-white/50 rounded-3xl">
                {getKPIIcon('humidity')}
              </div>
              <div className="ml-4">
                <p className="text-lg font-medium text-gray-600">Avg Humidity</p>
                <p className="text-2xl md:text-3xl font-bold text-black">
                  {Math.round(filteredLocationData.reduce((sum, loc) => sum + loc.latest.humidity_percent, 0) / filteredLocationData.length)}%
                </p>
              </div>
            </div>
          </div>

          <div className="p-6 rounded-3xl shadow-lg h-32 md:h-32 lg:h-32">
            <div className="flex items-center">
              <div className="p-6 bg-white/50 rounded-3xl">
                {getKPIIcon('wind')}
              </div>
              <div className="ml-4">
                <p className="text-lg md:text-lg font-medium text-gray-600">Avg Wind Speed</p>
                <p className="text-2xl md:text-3xl font-bold text-black">
                  {Math.round(filteredLocationData.reduce((sum, loc) => sum + loc.latest.wind_speed_ms, 0) / filteredLocationData.length)} m/s
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Weather Cards - flex-grow to fill remaining space */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6 flex-grow">
          {displayData.map((locationData: WeatherData) => (
            <div 
              key={locationData.location} 
              className="rounded-3xl shadow-xl overflow-hidden hover:shadow-lg transition-shadow duration-300 flex flex-col h-full relative"
            >
              {/* Background image overlay with reduced overlay */}
              {getLocationImage(locationData.location) && (
                <div className="absolute inset-0 z-0">
                  <img 
                    src={getLocationImage(locationData.location)} 
                    alt={locationData.location} 
                    className="w-full h-full object-cover"
                  />
                  {/* Light overlay to make text readable */}
                  <div className="absolute inset-0 bg-white bg-opacity-80"></div>
                </div>
              )}
              
              {/* Content on top of background */}
              <div className="relative z-10 flex flex-col h-full justify-end">
                <div className="p-3 md:p-4">
                  <div className="flex justify-between items-center">
                    <h2 className="text-4xl md:text-5xl font-extrabold text-black">{locationData.location}</h2>
                    {getWeatherIcon(locationData.weather_main)}
                  </div>
                </div>
                <div className="p-4 md:p-6 flex flex-col">
                  <div className="flex justify-between items-center mb-3 md:mb-4">
                    <span className="text-4xl md:text-5xl font-bold text-black">{Math.round(locationData.temperature_celsius)}°C</span>
                    <span className="text-2xl md:text-3xl font-semibold text-black">Feels like {Math.round(locationData.feels_like_celsius)}°C</span>
                  </div>
                  <div className="space-y-2">
                    <div className="flex justify-between text-2xl md:text-2xl">
                      <span className="text-black font-bold">Humidity:</span>
                      <span className="font-semibold">{locationData.humidity_percent}%</span>
                    </div>
                    <div className="flex justify-between text-2xl md:text-2xl">
                      <span className="text-black font-bold">Wind Speed:</span>
                      <span className="font-semibold">{locationData.wind_speed_ms} m/s</span>
                    </div>
                    <div className="flex justify-between text-2xl md:text-2xl">
                      <span className="text-black font-bold">Pressure:</span>
                      <span className="font-semibold">{locationData.pressure_hpa} hPa</span>
                    </div>
                    <div className="flex justify-between text-2xl md:text-2xl">
                      <span className="text-black font-bold">Visibility:</span>
                      <span className="font-semibold">{Math.round(locationData.visibility_meters / 1000)} km</span>
                    </div>
                    <div className="flex justify-between text-2xl md:text-2xl">
                      <span className="text-black font-bold">Conditions:</span>
                      <span className="font-semibold capitalize">{locationData.weather_description}</span>
                    </div>
                  </div>
                  <div className="mt-3 md:mt-4 text-2xl text-gray-500">
                    Last updated: {formatTime(locationData.timestamp)}
                  </div>

                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;