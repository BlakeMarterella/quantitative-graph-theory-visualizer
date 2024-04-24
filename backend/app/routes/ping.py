"""
File containing API resource details for the 'ping' namespace.
"""
from flask_api import status
from flask_restx import Namespace, Resource
from app.api_schemas import BasicResponseSchema
from app.constants import API_PREFIX, ONLINE, EHttpMessages


# Setup API namespace for the endpoint: "/api/ping"
ping_ns = Namespace(
    'ping', 
    description="Ping Endpoint", 
    path="/ping"
)


# Create the Resource.
@ping_ns.route("")
@ping_ns.response(code=status.HTTP_401_UNAUTHORIZED, description=EHttpMessages.UNAUTHORIZED, model=BasicResponseSchema)                     # Just playing around with these for now.
@ping_ns.response(code=status.HTTP_500_INTERNAL_SERVER_ERROR, description=EHttpMessages.INTERNAL_SERVER_ERROR, model=BasicResponseSchema)   # Just playing around with these for now.
class PingApi(Resource):
    """Class defining the methods for the "/api/hello" endpoint."""
    api_endpoint = API_PREFIX + "/ping"
    
    @ping_ns.doc("ping_get")
    @ping_ns.response(code=status.HTTP_200_OK, description=EHttpMessages.SUCCESS, model=BasicResponseSchema)
    @ping_ns.marshal_with(BasicResponseSchema)
    def get(self):
        """Register GET method.
        
        Ping endpoint to make sure the app is still alive.
        
        Return:
            BasicResponse
        """
        return {
            "message": EHttpMessages.SUCCESS,
            "data": ONLINE
        }      
