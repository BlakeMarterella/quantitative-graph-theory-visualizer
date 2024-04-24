from dotenv import load_dotenv, find_dotenv
from app import create_app, ConfigVars
from flask import abort, request, make_response, g
from app.constants import EClientErrorMessages

# Load environment variable from the .env file (if it exists)
_env_file = find_dotenv()
if _env_file:
    load_dotenv(_env_file)
        
# Create a new flask app
app = create_app()

@app.before_request
def before_request_callback():
    """Function that gets called before every inbound request.
    
    We are doing things like handling Flask's CORS preflight and firebase 
    authentication here.
    
    Returns:
        Void.
    """
    headers = request.headers
    
    # Handle Flask's CORS Preflight
    if request.method in ["OPTIONS"]:
        origin_header = headers.get('Origin')
        allowed_origins = ConfigVars.get_ALLOWED_ORIGINS()
        app.logger.debug(f"Received OPTIONS request. Checking that the request " + 
                         f"Origin, '{origin_header}', is a part of our " + 
                         f"ALLOWED_ORIGINS, '{allowed_origins}'.")
        if origin_header in allowed_origins:
            response = make_response()
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.headers.add('Access-Control-Allow-Headers', "*")
            response.headers.add('Access-Control-Allow-Methods', "*")
            return response
        else:
            abort(400, EClientErrorMessages.CROSS_SITE_SCRIPTING)
    
    # Logging some details about the request.
    if request.method in ["GET"]:
        params = {key:value for key, value in request.args.items()}
        data = f"Query Params: {params}"
    elif "Content-Type" in headers and "multipart/form-data" in headers["Content-Type"]:
        data = "UPLOADING A FILE"
    else:
        if not request.is_json:
            abort(400, EClientErrorMessages.INVALID_JSON_PROVIDED)
        json_data = request.get_json()
        data = f"Payload: {json_data}"
        

@app.after_request
def after_request_callback(response):
    """Function that gets called right before sending the response back to the 
    client.
    
    We can make any last minute adjustments or changes to the response before it
    gets sent back to the client.
    
    Args:
        response:
            A Flask Response object that is en-route back to the client.
    
    Returns:
        The response arg, but modified.
    """
    g.user = None   # Rest the session's 'user' value after a request is fulfilled no matter what.
    response.headers["Access-Control-Allow-Origin"] = "*"   # CORS related.
    return response

if __name__ == '__main__':
    # Start the Flask application.
    app.run(host="0.0.0.0", port=ConfigVars.get_PORT())