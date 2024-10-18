from django.test import TestCase
from unittest.mock import patch, MagicMock

import requests
from api.services import OpenWeatherMapService

class OpenWeatherMapServiceTests(TestCase):
    @patch('api.services.requests.get')
    def test_get_weather_data_success(self, mock_get):
        # Mock API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'cod': '200', 'list': []}
        mock_get.return_value = mock_response

        service = OpenWeatherMapService(api_key='test_api_key')
        result = service.get_weather_data('London')

        self.assertEqual(result['cod'], '200')
        mock_get.assert_called_once()

    @patch('api.services.requests.get')
    def test_get_weather_data_city_not_found(self, mock_get):
        # Mock API response with city not found (404)
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"cod": "404", "message": "City not found"}
        mock_get.return_value = mock_response

        service = OpenWeatherMapService(api_key='test_api_key')
        result = service.get_weather_data('UnknownCity')

        self.assertEqual(result['cod'], '404')
        self.assertEqual(result['message'], 'City not found')

    @patch('api.services.requests.get')
    def test_get_weather_data_http_error(self, mock_get):
        # Mock an HTTPError being raised
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("API Error")
        mock_get.return_value = mock_response

        service = OpenWeatherMapService(api_key='test_api_key')
        result = service.get_weather_data('London')

        self.assertEqual(result['cod'], 'error')
        self.assertIn('Failed to retrieve weather data', result['message'])
