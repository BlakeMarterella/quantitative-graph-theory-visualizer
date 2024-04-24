"""
Configuration file for the LOCAL environment.

Used for local development and testing.
"""
import os

ENV = "PROD"
PORT = os.getenv("PORT", 8080)
DEBUG = False
ALPHA_API_KEY = os.getenv("ALPHA_API_KEY")
ALLOWED_ORIGINS = ["http://localhost:3000", "http://localhost:5000"]