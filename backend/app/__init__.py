"""
Contains the Flask create_app() function along with any other Flask app 
initialization functions.
"""
import os
from flask import Flask
from flask_cors import CORS
from flask_restx import Api

from app.constants import EEnvironments, API_PREFIX
from config.ext.helper import ConfigVarHelper

# Create a global variable, ConfigVars, that can be used anywhere in the 
# application to get or set application config variables.
ConfigVars: ConfigVarHelper = ConfigVarHelper()

def create_app():
    """Creates and returns a fully initialized Flask application object.
    
    Returns:
        A configured Flask app.
    """
    global ConfigVars, FirebaseApp, Firestore
    
    app = Flask(__name__)
    
    # Load the default configuration followed by the environment specific configuration.
    environment = os.getenv('ENV').upper()  # Usually we'd use the ConfigVars object, but this is too soon in app start up.
    app.config.from_object('config.default')
    app.config.from_object(get_environment_specific_config_object(environment))
    
    # Initialize the ConfigVars global variable.
    ConfigVars.set_flask_app(app=app)
    
    # Initialize the Api and metadata.
    # authorizations = {
    #     'apiKey': {
    #         'type': "apiKey",
    #         'in': "header",
    #         'name': "X_API_TOKEN"   # Required by all requests needing authentication.
    #     }
    # }
    api = Api(
        app, 
        version="1.0",
        title="Quantative Graph Theory API",
        description="Utility to make graph theory calculations within finance easier by providing access to historical stock datasets and other financial data.",
        prefix=API_PREFIX,
        # authorizations=authorizations,
        default_mediatype="application/json"
    )
    register_api_schemas(api=api)
    register_api_namespaces(api=api, environment=environment)
    register_errorhandlers(app=app)
    
    # Setup CORS.
    CORS(
        app,
        supports_credentials=True,
        resources={r"/*": {"origins": ConfigVars.get_ALLOWED_ORIGINS()}}
    )
    
    return app


def register_api_schemas(api: Api) -> None:
    """Dedicated function to registering all flask_restx API schemas with the 
    app's Api.
    
    This essentially creates the shared schemas for the app.
    
    Args:
        api:
            The flask_restx Api object to register the schemas with.
    
    Returns:
        Void.
    """
    # Register all schemas that need to be registered :)
    from app.api_schemas import SCHEMAS_TO_REGISTER
    for schema in SCHEMAS_TO_REGISTER:
        api.models[schema.name] = schema
    
    
def register_api_namespaces(api: Api, environment: str = EEnvironments.LOCAL) -> None:
    """Dedicated function to registering all flask_restx API namespaces with 
    the app's Api.
    
    This essentially creates the endpoints for the app.
    
    Args:
        api (Api): The flask_restx Api object to register the namespaces with.
        environment (str): The environment the app is running in.
    
    Returns:
        Void.
    """
    from app.routes import NAMESPACES_TO_REGSITER 
    for namespace in NAMESPACES_TO_REGSITER:
        api.add_namespace(namespace)
        

def register_errorhandlers(app: Flask):
    from app.exceptions import BadRequestException, UnauthorizedException, \
        InternalServerErrorException, NotFoundException
    
    @app.errorhandler(BadRequestException)
    def handle_bad_request(exception):
        return exception.api_response
    
    @app.errorhandler(UnauthorizedException)
    def handle_unauthorized(error):
        return error.api_response
    
    @app.errorhandler(NotFoundException)
    def handle_not_found(error):
        return error.api_response
    
    @app.errorhandler(InternalServerErrorException)
    def handle_internal_server_error(exception):
        return exception.api_response


def get_environment_specific_config_object(environment: str) -> str:
    """Returns the Flask config object depending on the environment.
    
    For example, if we are running the application for the DEV environment, then
    the config object path, 'backend/config/dev.py', will be returned.
    
    Args:
        environment (str): The environment the application is running in.
    
    Returns:
        A string representing the path to a config object.
    """
    if environment == EEnvironments.LOCAL:
        return 'config.local'
    elif environment == EEnvironments.PROD:
        return 'config.prod'
    else:
        raise Exception(f"Unknown application environment, '{environment}'. " \
            f"Can't load configuration.")