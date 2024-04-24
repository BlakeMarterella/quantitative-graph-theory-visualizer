"""
File containing application specific constants.
"""
from flask import jsonify
from flask_api import status


UNSET = "UNSET"
ONLINE = "Online"
OFFLINE = "Offline"
API_PREFIX = "/"

class EEnvironments:
    """
    Enum class containing all the available application environment constants.
    """
    LOCAL   = "LOCAL"
    PROD    = "PROD"
    ALL     = [LOCAL, PROD]


class EClientErrorMessages:
    """
    Enum class containing all error message constants that could be sent back 
    to a Client.
    """
    CROSS_SITE_SCRIPTING = "Are you trying to attack me using cross site scripting?"
    INVALID_JSON_PROVIDED = "Invalid JSON provided."
    UNAUTHORIZED = "Unauthorized request"
    NOT_FOUND = "The resource you are looking for could not be found"
    INTERNAL_SERVER_ERROR = "Internal Server Error"


class EHttpMessages:
    """
    Enum class containing all HTTP message constants that could be sent back to 
    a client with the Response.
    """
    SUCCESS = "Success" # code == 200
    UPDATED = "Updated" # code == 200
    CREATED = "Created" # code == 201
    BAD_REQUEST = "Bad Request" # code == 400
    UNAUTHORIZED = "Unauthorized" # code == 401
    NOT_FOUND = "Not Found" # code == 404
    INTERNAL_SERVER_ERROR = "Internal Server Error" # code == 500


class ApiResponse:
    def __new__(cls, message: str, data: any, status_code: status):
        """Wrapper for our API responses.
        
        This ensures that all the required response fields are returned with 
        each request. 
        
        Args:
            message: (str) The message of the response.
            data: (any) The data of the response.
            status_code: (flask_api.status) The corresponding HTTP status code
                for the response.
        
        Returns:
            A flask.jsonify object containing the response payload in the proper 
            format and the response's status code.
        """
        return {
            "message": message,
            "data": data
        }, status_code
        
