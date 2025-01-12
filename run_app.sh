#!/bin/bash

# Script to run the FastAPI application

# Define variables
APP_NAME="app.main:app"
HOST="127.0.0.1"
PORT="8000"
WORKERS=1
LOG_LEVEL="debug"

# Activate virtual environment if exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Install dependencies if not already installed
echo "Checking and installing dependencies..."
pip install -r requirements.txt

# Run the FastAPI app using uvicorn with DEBUG log level
echo "Starting the FastAPI application with log level DEBUG..."
uvicorn $APP_NAME --host $HOST --port $PORT --workers $WORKERS --log-level $LOG_LEVEL
