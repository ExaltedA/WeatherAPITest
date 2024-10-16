
# 🌦 Weather Forecast Web App - Interview Task

This project is a **weather forecast web application** built as part of an interview task. It allows users to search for the weather forecast of any city using the OpenWeatherMap API. The app provides a daily forecast for the next five days, with the option to view detailed hourly data for each day.

## 📋 Task Objective

The purpose of this task was to demonstrate proficiency in:
- **Django and Django REST Framework** for backend API development.
- **Frontend development** using HTML, CSS, and JavaScript.
- **Integration of external APIs**, specifically the OpenWeatherMap API.
- **Caching** using Redis to improve performance.
- **Docker** for containerized development and deployment.
- **Gunicorn** for handling concurrency in production.

## 🚀 How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/your-username/weather-forecast-app.git
cd weather-forecast-app
```

### 2. Install dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

### 3. Set up your environment

Create a `.env` file in the root directory with the following content:

```
OPENWEATHERMAP_API_KEY=your_api_key_here
```

Make sure to replace `your_api_key_here` with your actual OpenWeatherMap API key.

### 4. Run the app using Docker

The project is Dockerized for ease of deployment. To run everything (Django, Redis, PostgreSQL, and Gunicorn) via Docker, use:

```bash
docker-compose up --build
```

### 5. Run locally without Docker (if needed)

To run the app locally without Docker:

1. Start the Django server:
    ```bash
    python manage.py runserver
    ```

2. Access the app at `http://127.0.0.1:8000`.

### 6. Running with Gunicorn

To run the app in a production-like environment using **Gunicorn**, it's all set up within the Docker container. Gunicorn is configured using the `gunicorn_config.py` file. The number of workers and binding details can be found there.

You can also modify the `Dockerfile` or `docker-compose.yml` to adjust Gunicorn parameters. The current command for running Gunicorn inside the Docker container is:

```bash
gunicorn --workers 3 --bind 0.0.0.0:8000 weatherAPI.wsgi:application
```

## 🌐 Features

### Core Features:
- **City-based Weather Search**: Search any city to get its weather forecast for the next 5 days.
- **Daily Weather Forecast**: Provides average temperature, minimum and maximum temperatures, pressure, humidity, and wind speed.
- **Hourly Weather Forecast**: View hourly weather details for any day by clicking "Show Hourly".
- **Weather Icons**: Displays visual weather conditions with OpenWeatherMap’s built-in icons.

### Backend:
- **Django REST Framework**: RESTful API for fetching weather data.
- **OpenWeatherMap Integration**: Fetches real-time data using OpenWeatherMap's API.
- **Redis Caching**: Weather data is cached for 30 minutes to optimize API calls and reduce latency.

### Frontend:
- **Dynamic UI**: Clean and user-friendly interface with interactive elements (e.g., expanding hourly forecast).
- **JavaScript for Dynamic Behavior**: Uses JavaScript to fetch data asynchronously and update the UI dynamically.

## 🌍 URLs

Here are the main URLs for interacting with the web app and its API:

- **`/`**: The homepage with a search form to look up weather forecasts.
- **`/forecast/<city_name>/`**: Returns the weather forecast data for a specified city in JSON format. Example:
  ```
  /forecast/London/
  ```

- **`/admin/`**: Access to the Django admin panel for managing the application.

### Example Workflow:
1. Visit the homepage (`/`), enter a city name (e.g., "London"), and submit the form.
2. The app will display the 5-day weather forecast, along with hourly details for each day.
3. You can click the "Show Hourly" button for each day to expand and see hourly weather details.

## 💻 Technologies

- **Backend**: Django, Django REST Framework
- **Frontend**: HTML, CSS, JavaScript
- **Caching**: Redis (for API response caching)
- **Database**: PostgreSQL (configured in Docker)
- **API**: OpenWeatherMap API for weather data
- **Containerization**: Docker for easy setup and deployment
- **Concurrency**: Gunicorn for handling multiple requests

## 📂 Project Structure

```plaintext
weatherAPI/
├── api/
│   ├── apps.py
│   ├── cache_service.py
│   ├── models.py
│   ├── serializers.py
│   ├── services.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── templates/
│   └── weather_search.html
├── weatherAPI/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── .dockerignore
├── .env
├── .env.example
├── .gitignore
├── db.sqlite3
├── docker-compose.yml
├── Dockerfile
├── django_debug.log
├── gunicorn_config.py
├── manage.py
└── requirements.txt
```