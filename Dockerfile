# Use a base Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire folder into the container
COPY flask1/ .

# Expose port 5000 for the Flask app
EXPOSE 5000

# Set the environment variable to prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# Set the environment variable for Flask
ENV FLASK_APP=app.py

# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]