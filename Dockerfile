# Use the official Python image
FROM python:3.13-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the FastAPI port
EXPOSE 8000

# Run the database initialization script and then start the FastAPI application
CMD ["sh", "-c", "python database/database.py && uvicorn main:app --host localhost --port 8000 --reload"]