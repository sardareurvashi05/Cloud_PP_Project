FROM python:3.9-slim

# Set working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Upgrade pip in the container
RUN pip install --upgrade pip

# Install PostgreSQL development libraries
RUN apt-get update && apt-get install -y libpq-dev

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . /app/

# Expose the port for the Django app
EXPOSE 8000

# Command to run the Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
