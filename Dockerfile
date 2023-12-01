FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy the local directory contents into the container
COPY . .

# Install dependencies
RUN pip3 install -r requirements.txt

# Make migrations and migrate
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
