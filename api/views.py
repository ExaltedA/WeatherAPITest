import logging
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import WeatherForecastSerializer
from .services import OpenWeatherMapService, WeatherService
from .cache_service import CacheService

# Create a logger instance for this module
logger = logging.getLogger(__name__)


class PingPongView(APIView):
    def get(self, request):
        data = {"message": "Pong"}
        return Response(data)


class WeatherSearchView(APIView):
    def get(self, request):
        return render(request, 'weather_search.html')


class WeatherForecastView(APIView):
    def __init__(self, weather_service: WeatherService = None, cache_service: CacheService = None):
        """Inject dependencies for weather service and cache service."""
        self.weather_service = weather_service or OpenWeatherMapService()
        self.cache_service = cache_service or CacheService()

    def get(self, request, city_name, format=None):
        """Handles GET requests to retrieve weather forecast."""
        logger.debug(f"Received request for weather forecast in city: {city_name}")

        # Define a unique cache key for the city
        cache_key = f"weather_{city_name}"

        # Try to retrieve cached data
        cached_data = self.cache_service.get_cached_data(cache_key)
        if cached_data:
            logger.debug(f"Cache hit for {city_name}, serving cached data")
            return Response(cached_data)

        logger.debug(f"Cache miss for {city_name}, fetching new data from API")

        # Fetch data from the weather service
        data = self.weather_service.get_weather_data(city_name)
        if data.get('cod') != '200':
            error_message = data.get('message', 'Unknown error occurred while fetching weather data')
            logger.error(f"Error fetching weather data: {error_message}")
            return Response({"error": error_message}, status=400)

        # Parse the data with the service's method
        daily_forecasts, error_message = self.weather_service.parse_weather_data(data)
        if error_message:
            logger.error(f"Error parsing weather data: {error_message}")
            return Response({"error": error_message}, status=400)

        # Serialize the data
        serializer = WeatherForecastSerializer(daily_forecasts, many=True)
        response_data = serializer.data

        # Cache the serialized data for 30 minutes (1800 seconds)
        if self.cache_service.set_cached_data(cache_key, response_data, timeout=1800):
            logger.debug(f"Successfully cached data for {city_name} with key {cache_key}")
        else:
            logger.warning(f"Failed to cache data for {city_name}")

        return Response(response_data)