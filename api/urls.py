from django.urls import path
from .views import WeatherForecastView, WeatherSearchView, PingPongView

urlpatterns = [
    path('ping-pong/', PingPongView.as_view(), name='ping-pong'),
    path('forecast/<str:city_name>/', WeatherForecastView.as_view(), name='weather-forecast'),
]