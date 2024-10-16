from rest_framework import serializers

class TwoDecimalPlacesFloatField(serializers.FloatField):
    """Custom FloatField that ensures float values are formatted to two decimal places."""
    def to_representation(self, value):
        """Override the representation to format floats with two decimal places."""
        value = super().to_representation(value)
        return format(value, ".2f")  # Format to two decimal places

# Serializer to handle hourly weather data
class HourlyForecastSerializer(serializers.Serializer):
    time = serializers.CharField()

    # Use TwoDecimalPlacesFloatField to ensure two decimal places
    temperature = TwoDecimalPlacesFloatField()
    temperature_min = TwoDecimalPlacesFloatField()
    temperature_max = TwoDecimalPlacesFloatField()
    pressure = TwoDecimalPlacesFloatField()
    humidity = TwoDecimalPlacesFloatField()
    wind_speed = TwoDecimalPlacesFloatField()
    description = serializers.CharField()
    icon = serializers.CharField() 

# Serializer to handle daily weather data, including hourly data
class WeatherForecastSerializer(serializers.Serializer):
    date = serializers.CharField()

    # Use TwoDecimalPlacesFloatField for daily summary fields
    temperature_avg = TwoDecimalPlacesFloatField()
    temperature_min = TwoDecimalPlacesFloatField()
    temperature_max = TwoDecimalPlacesFloatField()
    
    hourly_forecasts = HourlyForecastSerializer(many=True)  # Nested serializer for hourly data
