bind = "0.0.0.0:8000"
workers = 3  # Set the number of worker processes. Number of workers: 2 x (number of CPU cores) + 1
timeout = 120  # Set the timeout to avoid killing long requests
accesslog = "-"  # Log access to stdout (console)
errorlog = "-"  # Log errors to stdout (console)