import requests
import logging
from django.conf import settings
from datetime import datetime, timezone
from collections import defaultdict
from typing import List, Dict, Tuple, Optional

logger = logging.getLogger(__name__)

class WeatherService:
    """Abstract base class for weather services."""
    
    def get_weather_data(self, city_name: str) -> Dict:
        """Fetches raw weather data for a city."""
        raise NotImplementedError

    def parse_weather_data(self, data: Dict) -> Tuple[Optional[List[Dict]], Optional[str]]:
        """Parses weather data and returns structured data."""
        raise NotImplementedError


class OpenWeatherMapService(WeatherService):
    """Concrete class for fetching weather data from OpenWeatherMap API."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.OPENWEATHERMAP_API_KEY

    def get_weather_data(self, city_name: str) -> Dict:
        """Fetches weather data from OpenWeatherMap API."""
        
        url = self._build_api_url(city_name)
        return self._make_api_request(url, city_name)

    def parse_weather_data(self, data: Dict) -> Tuple[Optional[List[Dict]], Optional[str]]:
        """Parses raw weather data from OpenWeatherMap and returns daily grouped forecasts."""
        
        if data.get('cod') != '200':
            return None, data.get('message')

        # Group the forecast by day
        forecast_by_day = self._group_forecasts_by_day(data['list'])

        # Prepare the final grouped data by day
        daily_forecasts = []
        for date, hourly_forecasts in forecast_by_day.items():
            daily_summary = self._generate_daily_summary(date, hourly_forecasts)
            daily_forecasts.append(daily_summary)

        return daily_forecasts, None

    def _build_api_url(self, city_name: str) -> str:
        """Helper function to build the API URL."""
        return f"http://api.openweathermap.org/data/2.5/forecast?q={city_name}&units=metric&appid={self.api_key}"

    def _make_api_request(self, url: str, city_name: str) -> Dict:
        """Helper function to make the API request and handle errors."""
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        
        except requests.HTTPError as http_err:
            if response.status_code == 404:
                logger.warning(f"City not found: {city_name}")
                return {"cod": "404", "message": "City not found. Please check the city name and try again."}
            
            logger.error(f"HTTP error occurred: {http_err}")
            return {"cod": "error", "message": "Failed to retrieve weather data. Please try again later."}
        
        except requests.RequestException as req_err:
            logger.error(f"An error occurred: {req_err}")
            return {"cod": "error", "message": "An unexpected error occurred. Please try again later."}

    def _group_forecasts_by_day(self, forecast_list: List[Dict]) -> Dict[str, List[Dict]]:
        """Groups hourly forecasts by day."""
        
        forecast_by_day = defaultdict(list)
        for forecast in forecast_list:
            date = self._timestamp_to_date(forecast['dt'])
            time = self._timestamp_to_time(forecast['dt'])
            
            # Extract the weather icon and other weather details
            weather_info = forecast['weather'][0]  # This contains the weather array (with 'icon')
            icon = weather_info.get('icon')  # Extract the icon code

            forecast_by_day[date].append({
                'time': time,
                'temperature': forecast['main']['temp'],
                'temperature_min': forecast['main']['temp_min'],
                'temperature_max': forecast['main']['temp_max'],
                'pressure': forecast['main']['pressure'],
                'humidity': forecast['main']['humidity'],
                'wind_speed': forecast['wind']['speed'],
                'description': forecast['weather'][0]['description'],
                'icon': icon
            })
        return forecast_by_day

    def _generate_daily_summary(self, date: str, hourly_forecasts: List[Dict]) -> Dict:
        """Generates a summary for the day's weather forecast."""
       
        temperatures = [hour['temperature'] for hour in hourly_forecasts]
        min_temps = [hour['temperature_min'] for hour in hourly_forecasts]
        max_temps = [hour['temperature_max'] for hour in hourly_forecasts]

        return {
            'date': date,
            'temperature_avg': sum(temperatures) / len(temperatures),
            'temperature_min': min(min_temps),
            'temperature_max': max(max_temps),
            'hourly_forecasts': hourly_forecasts  # Include all hourly data for the day
        }

    def _timestamp_to_date(self, timestamp: int) -> str:
        """Converts a Unix timestamp to a 'YYYY-MM-DD' formatted date string."""
        return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime('%Y-%m-%d')

    def _timestamp_to_time(self, timestamp: int) -> str:
        """Converts a Unix timestamp to a 'HH:MM:SS' formatted time string."""
        return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime('%H:%M:%S')
