"""
Entry point to the app.schemas module.

Helpful definitions:
    API Model:  A declarative schema used by SwaggerUI and endpoints for 
                marshalling incoming and outgoing data.
    Schema:     A declarative schema used by the application for serializing and 
                deserializing data going to and coming from our Firestore.
"""
from .historical_stock_data import HistoricalStockDataDocumentSchema, HistoricalStockDataDocumentApiModel, HistoricalStockDataFields 