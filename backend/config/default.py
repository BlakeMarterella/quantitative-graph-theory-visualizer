"""
Default configuration file for the Flask application. It contains all the 
required environment variables for the application to run, however, some of the 
variables may be overridden by the other environment-specific config files 
(i.e., local.py).
"""
import os

# Set the specified environment, LOCAL by default
ENV = os.getenv("ENV", "LOCAL").upper()
# Set the Port, 8080 by default
PORT = os.getenv("PORT", 8080)
# Set the Debug mode, True by default for local dev
DEBUG = True
# Get the API key
ALPHA_API_KEY = os.getenv("ALPHA_API_KEY")
# Configuret the allowed origins for CORS
ALLOWED_ORIGINS = ["http://localhost:3000", "http://localhost:5000"]