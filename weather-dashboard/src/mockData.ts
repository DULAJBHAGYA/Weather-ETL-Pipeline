export interface WeatherData {
  id: number;
  location: string;
  timestamp: string;
  temperature_celsius: number;
  feels_like_celsius: number;
  humidity_percent: number;
  pressure_hpa: number;
  wind_speed_ms: number;
  visibility_meters: number;
  weather_main: string;
  weather_description: string;
  clouds_percent: number;
  rain_1h_mm: number | null;
  snow_1h_mm: number | null;
}

export const mockWeatherData: WeatherData[] = [
  {
    id: 1,
    location: "Kandy",
    timestamp: "2023-06-15T14:30:00Z",
    temperature_celsius: 24.5,
    feels_like_celsius: 26.1,
    humidity_percent: 75,
    pressure_hpa: 1010,
    wind_speed_ms: 2.2,
    visibility_meters: 8000,
    weather_main: "Clouds",
    weather_description: "Broken clouds",
    clouds_percent: 65,
    rain_1h_mm: null,
    snow_1h_mm: null
  },
  {
    id: 2,
    location: "Colombo",
    timestamp: "2023-06-15T14:30:00Z",
    temperature_celsius: 28.2,
    feels_like_celsius: 32.8,
    humidity_percent: 82,
    pressure_hpa: 1008,
    wind_speed_ms: 3.5,
    visibility_meters: 6000,
    weather_main: "Rain",
    weather_description: "Light rain",
    clouds_percent: 90,
    rain_1h_mm: 0.8,
    snow_1h_mm: null
  },
  {
    id: 3,
    location: "Anuradhapura",
    timestamp: "2023-06-15T14:30:00Z",
    temperature_celsius: 39.8,
    feels_like_celsius: 42.1,
    humidity_percent: 48,
    pressure_hpa: 1015,
    wind_speed_ms: 4.1,
    visibility_meters: 12000,
    weather_main: "Clear",
    weather_description: "Sunny",
    clouds_percent: 5,
    rain_1h_mm: null,
    snow_1h_mm: null
  },
  {
    id: 4,
    location: "Kandy",
    timestamp: "2023-06-15T13:30:00Z",
    temperature_celsius: 23.8,
    feels_like_celsius: 25.4,
    humidity_percent: 77,
    pressure_hpa: 1011,
    wind_speed_ms: 2.0,
    visibility_meters: 7500,
    weather_main: "Clouds",
    weather_description: "Scattered clouds",
    clouds_percent: 45,
    rain_1h_mm: null,
    snow_1h_mm: null
  },
  {
    id: 5,
    location: "Colombo",
    timestamp: "2023-06-15T13:30:00Z",
    temperature_celsius: 27.9,
    feels_like_celsius: 32.6,
    humidity_percent: 84,
    pressure_hpa: 1007,
    wind_speed_ms: 3.2,
    visibility_meters: 5800,
    weather_main: "Rain",
    weather_description: "Moderate rain",
    clouds_percent: 95,
    rain_1h_mm: 1.5,
    snow_1h_mm: null
  },
  {
    id: 6,
    location: "Anuradhapura",
    timestamp: "2023-06-15T13:30:00Z",
    temperature_celsius: 39.2,
    feels_like_celsius: 41.6,
    humidity_percent: 50,
    pressure_hpa: 1014,
    wind_speed_ms: 3.8,
    visibility_meters: 13000,
    weather_main: "Clear",
    weather_description: "Sunny",
    clouds_percent: 3,
    rain_1h_mm: null,
    snow_1h_mm: null
  }
];

export interface LocationWeatherData {
  location: string;
  latest: WeatherData;
  history: WeatherData[];
}

export const mockLocationData: LocationWeatherData[] = [
  {
    location: "Kandy",
    latest: mockWeatherData[0],
    history: [mockWeatherData[0], mockWeatherData[3]]
  },
  {
    location: "Colombo",
    latest: mockWeatherData[1],
    history: [mockWeatherData[1], mockWeatherData[4]]
  },
  {
    location: "Anuradhapura",
    latest: mockWeatherData[2],
    history: [mockWeatherData[2], mockWeatherData[5]]
  }
];