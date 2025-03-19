# Use the official Python image
FROM python:3.13-slim

RUN apt-get update 

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

EXPOSE 8005

# Run the database initialization script and then start the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8005"]
