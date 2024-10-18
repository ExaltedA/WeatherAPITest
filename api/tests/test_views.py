from django.test import TestCase
from unittest.mock import patch, MagicMock
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from api.views import WeatherForecastView
from api.services import OpenWeatherMapService

class PingPongViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_ping_pong(self):
        response = self.client.get(reverse('ping-pong'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"message": "Pong"})

class WeatherForecastViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch('api.services.OpenWeatherMapService.get_weather_data')
    @patch('api.cache_service.CacheService.get_cached_data')
    @patch('api.cache_service.CacheService.set_cached_data')
    def test_weather_forecast_cache_hit(self, mock_set_cache, mock_get_cache, mock_get_weather_data):
        # Mock cache hit (cache contains data)
        mock_get_cache.return_value = [{"date": "2024-10-17", "temperature_avg": 25.0}]
        
        response = self.client.get(reverse('weather-forecast', args=['London']))

        # Check the response and cache hit
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['date'], "2024-10-17")
        self.assertTrue(mock_get_cache.called)  # Ensure cache was checked
        self.assertFalse(mock_get_weather_data.called)  # Ensure API was not called due to cache hit

    @patch('api.services.OpenWeatherMapService.get_weather_data')
    @patch('api.cache_service.CacheService.get_cached_data')
    @patch('api.cache_service.CacheService.set_cached_data')
    def test_weather_forecast_cache_miss(self, mock_set_cache, mock_get_cache, mock_get_weather_data):
        # Mock cache miss (cache returns None, so API is called)
        mock_get_cache.return_value = None
        mock_get_weather_data.return_value = {
            'cod': '200',
            'list': [
                {
                    'dt': 1634486400,  # Example timestamp
                    'main': {'temp': 20.0, 'temp_min': 18.0, 'temp_max': 22.0, 'pressure': 1010, 'humidity': 80},
                    'weather': [{'description': 'clear sky', 'icon': '01d'}],
                    'wind': {'speed': 5.0}
                }
            ]
        }

        response = self.client.get(reverse('weather-forecast', args=['London']))

        # Check the response and cache miss
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['date'], '2021-10-17')
        self.assertTrue(mock_get_cache.called)  # Ensure cache was checked
        self.assertTrue(mock_get_weather_data.called)  # Ensure API was called due to cache miss
        self.assertTrue(mock_set_cache.called)  # Ensure the result is cached

    @patch('api.services.OpenWeatherMapService.get_weather_data')
    @patch('api.cache_service.CacheService.get_cached_data')
    @patch('api.cache_service.CacheService.set_cached_data')
    def test_weather_forecast_city_not_found(self, mock_set_cache, mock_get_cache, mock_get_weather_data):
        # Mock API returns a city not found error
        mock_get_cache.return_value = None
        mock_get_weather_data.return_value = {"cod": "404", "message": "City not found"}

        response = self.client.get(reverse('weather-forecast', args=['UnknownCity']))

        # Check the response for error
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "City not found")
