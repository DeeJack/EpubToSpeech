# Use the official Python image as a base
FROM python:3.11-slim

ENV PORT=5000
# ENV FLASK_APP=home.py
ENV HOST=0.0.0.0

# Set the working directory
WORKDIR /app

RUN mkdir -p database

# Copy the requirements file to install dependencies
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose the port the app runs on
# EXPOSE 5000

# Command to run the application
# CMD ["python", "home.py"]

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]