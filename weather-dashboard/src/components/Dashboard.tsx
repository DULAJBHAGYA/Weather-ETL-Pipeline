import React from 'react';
import { mockLocationData } from '../mockData';
import { IconType } from "react-icons";
import { FaLocationDot } from "react-icons/fa6";
import { RiTempColdFill } from "react-icons/ri";
import { MdWaterDrop } from "react-icons/md";
import { FaWind } from "react-icons/fa";

const Dashboard: React.FC = () => {
  const getWeatherIcon = (weatherMain: string) => {
    switch (weatherMain.toLowerCase()) {
      case 'clear':
        return '☀️';
      case 'clouds':
        return '☁️';
      case 'rain':
        return '🌧️';
      case 'snow':
        return '❄️';
      case 'thunderstorm':
        return '⛈️';
      default:
        return '🌈';
    }
  };

  const formatTime = (timestamp: string) => {
    return new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const formatDate = (timestamp: string) => {
    return new Date(timestamp).toLocaleDateString([], { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
  };

  // Filter to only show Kandy, Colombo, and Anuradhapura
  const filteredLocationData = mockLocationData.filter(location => 
    ['Kandy', 'Colombo', 'Anuradhapura'].includes(location.location)
  );

  return (
    <div className="min-h-screen bg-white p-4 md:p-6">
      <div className="max-w-7xl mx-auto w-[90%]">
        {/* Header */}
        <header className="mb-6 md:mb-8 text-left">
          <h1 className="text-2xl md:text-3xl lg:text-4xl font-semibold text-black mb-2">Weather Dashboard</h1>
          <p className="text-black text-sm md:text-base">Real-time weather monitoring for Kandy, Colombo, and Anuradhapura</p>
        </header>

        {/* Stats Overview */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6 md:mb-8">
          <div className="bg-white p-6 rounded-3xl shadow-lg">
            <div className="flex items-center">
              <div className="p-3 bg-green-100 rounded-2xl">
                <FaLocationDot className="w-6 h-6 text-green-400" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Locations Tracked</p>
                <p className="text-xl md:text-2xl font-bold text-black">{filteredLocationData.length}</p>
              </div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-3xl shadow-lg">
            <div className="flex items-center">
              <div className="p-3 bg-red-100 rounded-2xl">
                <RiTempColdFill className="w-6 h-6 text-red-400" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Avg Temperature</p>
                <p className="text-xl md:text-2xl font-bold text-black">
                  {Math.round(filteredLocationData.reduce((sum, loc) => sum + loc.latest.temperature_celsius, 0) / filteredLocationData.length)}°C
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-3xl shadow-lg">
            <div className="flex items-center">
              <div className="p-3 bg-blue-100 rounded-2xl">
                <MdWaterDrop className="w-6 h-6 text-blue-400" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Avg Humidity</p>
                <p className="text-xl md:text-2xl font-bold text-black">
                  {Math.round(filteredLocationData.reduce((sum, loc) => sum + loc.latest.humidity_percent, 0) / filteredLocationData.length)}%
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-3xl shadow-lg">
            <div className="flex items-center">
              <div className="p-3 bg-gray-100 rounded-2xl">
                <FaWind className="w-6 h-6 text-gray-400" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Avg Wind Speed</p>
                <p className="text-xl md:text-2xl font-bold text-black">
                  {Math.round(filteredLocationData.reduce((sum, loc) => sum + loc.latest.wind_speed_ms, 0) / filteredLocationData.length)} m/s
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Weather Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6 mb-6 md:mb-8">
          {filteredLocationData.map((locationData) => (
            <div 
              key={locationData.location} 
              className="bg-white rounded-3xl shadow-xl overflow-hidden hover:shadow-lg transition-shadow duration-300"
            >
              <div className="bg-white p-3 md:p-4">
                <div className="flex justify-between items-center">
                  <h2 className="text-lg md:text-xl font-semibold text-black">{locationData.location}</h2>
                  <span className="text-xl md:text-2xl">{getWeatherIcon(locationData.latest.weather_main)}</span>
                </div>
                <p className="text-gray-600 text-xs md:text-sm">{formatDate(locationData.latest.timestamp)}</p>
              </div>
              <div className="p-4 md:p-6">
                <div className="flex justify-between items-center mb-3 md:mb-4">
                  <span className="text-3xl md:text-4xl font-bold text-black">{locationData.latest.temperature_celsius}°C</span>
                  <span className="text-sm md:text-base text-gray-600">Feels like {locationData.latest.feels_like_celsius}°C</span>
                </div>
                <div className="space-y-2">
                  <div className="flex justify-between text-xs md:text-sm">
                    <span className="text-gray-700">Humidity:</span>
                    <span className="font-medium">{locationData.latest.humidity_percent}%</span>
                  </div>
                  <div className="flex justify-between text-xs md:text-sm">
                    <span className="text-gray-700">Wind Speed:</span>
                    <span className="font-medium">{locationData.latest.wind_speed_ms} m/s</span>
                  </div>
                  <div className="flex justify-between text-xs md:text-sm">
                    <span className="text-gray-700">Pressure:</span>
                    <span className="font-medium">{locationData.latest.pressure_hpa} hPa</span>
                  </div>
                  <div className="flex justify-between text-xs md:text-sm">
                    <span className="text-gray-700">Visibility:</span>
                    <span className="font-medium">{Math.round(locationData.latest.visibility_meters / 1000)} km</span>
                  </div>
                  <div className="flex justify-between text-xs md:text-sm">
                    <span className="text-gray-700">Conditions:</span>
                    <span className="font-medium capitalize">{locationData.latest.weather_description}</span>
                  </div>
                </div>
                <div className="mt-3 md:mt-4 text-xs text-gray-500">
                  Last updated: {formatTime(locationData.latest.timestamp)}
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