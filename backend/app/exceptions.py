"""
File containing application specific exceptions.
"""
from typing import Optional, Union
from flask import current_app as app
from flask_api import status
from app.constants import ApiResponse, EHttpMessages, EClientErrorMessages


class BaseRequestException(Exception):
    """
    Custom PARENT exception that lays the foundation for other request-related 
    exceptions that can be raised anywhere in the app as a way of immediately 
    returning the corresponding, formatted response to a client.
    """
    message: str = None
    data: any = None
    status_code: int = None
    api_response: ApiResponse = None
    
    def __init__(self):
        error_message = f"({self.message}, {self.status_code}): {self.data}"
        self.api_response = ApiResponse(
            message=self.message,
            data=self.data,
            status_code=self.status_code
        )
        if self.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR: 
            app.logger.critical(f"{error_message}", exc_info=True)
        else:
            app.logger.error(f"{error_message}")
        super().__init__(error_message)


class NotFoundException(BaseRequestException):
    """
    Custom exception that is raised when a requested resource can't be found.
    """
    def __init__(self, info: Optional[str] = None):
        self.message = EHttpMessages.NOT_FOUND
        self.data = info if info else EClientErrorMessages.NOT_FOUND
        self.status_code = status.HTTP_404_NOT_FOUND
        super().__init__()


class BadRequestException(BaseRequestException):
    """
    Custom exception that is raised when a client sends a bad request.
    """
    def __init__(self, error_message: Union[str, any]):
        self.message = EHttpMessages.BAD_REQUEST
        self.data = str(error_message)
        self.status_code = status.HTTP_400_BAD_REQUEST
        super().__init__()


class UnauthorizedException(BaseRequestException):
    """
    Custom exception that is raised when a client is not authorized.
    """
    def __init__(self, error_message: str = None):
        self.message = EHttpMessages.UNAUTHORIZED
        self.data = str(error_message) if error_message else EClientErrorMessages.UNAUTHORIZED
        self.status_code = status.HTTP_401_UNAUTHORIZED
        super().__init__()


class InternalServerErrorException(BaseRequestException):
    """
    Custom exception that is raised when there is an Internal Server Error.
    """
    def __init__(self, error_message: str = None):
        self.message = EHttpMessages.INTERNAL_SERVER_ERROR
        self.data = str(error_message) if error_message else EClientErrorMessages.INTERNAL_SERVER_ERROR
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        super().__init__()