#Dockerfile
FROM python:3.10-slim

# Set the environment variable for Python to not write bytecode
ENV PYTHONDONTWRITEBYTECODE=1\ 
    PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app  

# System deps (needed if you use mysqlclient, Pillow, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc default-libmysqlclient-dev pkg-config \
 && rm -rf /var/lib/apt/lists/  

# Copy the requirements file into the container
COPY requirements.txt /app/requirements.txt
# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Copy the rest of the application code into the container
COPY . /app/
# Expose the port the app runs on
EXPOSE 8000
# Set the environment variable for Django settings module
ENV DJANGO_SETTINGS_MODULE=alx_travel_app.settings


# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
