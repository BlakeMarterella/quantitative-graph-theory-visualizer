"""
Entry point for the 'resources' module.
"""
# All available resources.
from .ping import ping_ns
from .historical_stock_data import historical_stock_data_ns


"""
Export a list of the API namespaces we want to register with our API. This is 
used at app start and doing this makes management a bit easier.
"""
NAMESPACES_TO_REGSITER = [
    ping_ns,
    historical_stock_data_ns
]
