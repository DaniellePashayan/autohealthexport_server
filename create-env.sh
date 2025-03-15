#!/bin/bash

# Define the .env file path
ENV_FILE=".env"

# Check if the .env file already exists
if [ -f "$ENV_FILE" ]; then
    echo ".env file already exists. Skipping creation."
else
    echo "Creating .env file..."

    # Write environment variables to the .env file
    cat <<EOL > $ENV_FILE
# PostgreSQL Configuration
POSTGRES_USER=test_user
POSTGRES_PASSWORD=test_password
POSTGRES_DB=test_db
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# pgAdmin Configuration
PGADMIN_DEFAULT_EMAIL=admin@admin.com
PGADMIN_DEFAULT_PASSWORD=admin
EOL

    echo ".env file created successfully."
fi