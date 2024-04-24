"""
Configuration file for the LOCAL environment.

Used for local development and testing.
"""
import os

# Set the specified environment, LOCAL by default
ENV = "LOCAL" 
# Set the Port, 8080 by default
PORT = 8080
# Set the Debug mode, True by default for local dev
DEBUG = True
# Get the API key
ALPHA_API_KEY = os.getenv("ALPHA_API_KEY")
# Configuret the allowed origins for CORS
ALLOWED_ORIGINS = ["http://localhost:3000", "http://localhost:5000"]