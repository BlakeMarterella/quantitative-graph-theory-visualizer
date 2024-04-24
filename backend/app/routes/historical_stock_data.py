"""
File containing API resource details for the 'users' namespace.
"""
from flask import current_app as app
from flask_api import status
from flask_restx import Namespace, Resource
from marshmallow.exceptions import ValidationError

from app.api_schemas import (
    BadRequestResponseSchema,
    UnauthorizedResponseSchema,
    InternalServerErrorResponseSchema,
    HistoricalStockDataResponseSchema,
    HistoricalStockDataDocumentApiModel
)
from app.schemas import HistoricalStockDataDocumentSchema
from app.constants import (
    API_PREFIX,
    ApiResponse,
    EHttpMessages,
    EClientErrorMessages
)
from app.exceptions import BadRequestException, BaseRequestException


# Setup API namespace for the endpoint: "/api/users"
historical_stock_data_namespace_path = "/historical-stock-data"
historical_stock_data_ns = Namespace(
    'Historical Stock Data', 
    description="Endpoints for retrieving historical stock data.",
    path=historical_stock_data_namespace_path
)


@historical_stock_data_ns.route("")
@historical_stock_data_ns.response(code=status.HTTP_400_BAD_REQUEST, model=BadRequestResponseSchema, description=EHttpMessages.BAD_REQUEST)
@historical_stock_data_ns.response(code=status.HTTP_401_UNAUTHORIZED, model=UnauthorizedResponseSchema, description=EHttpMessages.UNAUTHORIZED)
@historical_stock_data_ns.response(code=status.HTTP_500_INTERNAL_SERVER_ERROR, model=InternalServerErrorResponseSchema, description=EHttpMessages.INTERNAL_SERVER_ERROR)
class HistoricalStockData(Resource):
    """Class defining the methods for the "/api/users" endpoint."""
    api_endpoint = API_PREFIX + historical_stock_data_namespace_path
    
    @historical_stock_data_ns.doc("data")
    @historical_stock_data_ns.response(code=status.HTTP_200_OK, model=HistoricalStockDataResponseSchema, description=EHttpMessages.SUCCESS)
    def get(self):
        """Retrieves historical stock data for the specified stock.
        
        Returns:
            BrotherDocuments: (List[Dict]) A list of all Users currently in the
                database.
        """
        try:
            return ApiResponse(
                message=EHttpMessages.SUCCESS,
                data="Hello World!",
                status_code=status.HTTP_200_OK
            )
        except BaseRequestException as request_exception:
            return request_exception.api_response
        except Exception as unknown_error:
            app.logger.critical(f"Unknown error occurred while trying to fulfill the 'list_users' request. Error: {str(unknown_error)}.", exc_info=True)
            return ApiResponse(
                message=EHttpMessages.INTERNAL_SERVER_ERROR, 
                data=EClientErrorMessages.INTERNAL_SERVER_ERROR,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
