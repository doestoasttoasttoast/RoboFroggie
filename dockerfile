# Use an official Python 3.10 image as the base image.
FROM python:3.11

# Set a working directory inside the container.
WORKDIR /app

# Copy the Python script from your local machine into the container.
COPY bot.py .
COPY event_handler.py .
COPY requirements.txt .
COPY .env .

# Install any Python dependencies if required.
# You can use a requirements.txt file if needed.
# Example: COPY requirements.txt .
#          RUN pip install -r requirements.txt
RUN pip install -r requirements.txt

# Define the command to run your Python script.
CMD ["python", "bot.py"]