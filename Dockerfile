FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

# Run Gunicorn with the configuration file
CMD ["gunicorn", "-c", "gunicorn_config.py", "weatherAPI.wsgi:application"]