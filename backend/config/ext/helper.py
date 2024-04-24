"""
File containing any helper classes, functions, and variables, etc.
"""
from flask import Flask
from app.constants import UNSET

class ConfigVarHelper:
    """
    Custom class providing abstraction and structure for accessing all 
    application specific environment variables.
    """
    flask_app: Flask = None

    def set_flask_app(self, app: Flask) -> None:
        """Sets the instance variable, flask_app, to the provided Flask app.
        
        This method must be called before you can use any of the other methods
        because they all rely on the instance variable, flask_app, which 
        contains all of the config variables they retrieve and set.
        
        Args:
            app:
                This application's Flask app object.
                
        Returns:
            Void.
        """
        self.flask_app = app
    
    # GETTER and SETTER methods for the ENV variable.
    def get_ENV(self) -> str:
        """Returns the environment variable, ENV."""
        return self.flask_app.config.get("ENV", UNSET)
    
    def set_ENV(self, new_value: str) -> None:
        """Sets a new value to the environment variable, ENV."""
        self.flask_app.config["ENV"] = new_value
    
    # GETTER and SETTER methods for the PORT variable.
    def get_PORT(self) -> str:
        """Returns the environment variable, PORT."""
        return self.flask_app.config.get("PORT", UNSET)

    def set_PORT(self, new_value: str) -> None:
        """Sets a new value to the environment variable, PORT."""
        self.flask_app.config["PORT"] = new_value

    # GETTER and SETTER methods for the DEBUG variable.
    def get_DEBUG(self) -> str:
        """Returns the environment variable, DEBUG."""
        return self.flask_app.config.get("DEBUG", UNSET)

    def set_DEBUG(self, new_value: str) -> None:
        """Sets a new value to the environment variable, DEBUG."""
        self.flask_app.config["DEBUG"] = new_value

    # GETTER and SETTER methods for the ALPHA_API_KEY variable.
    def get_ALPHA_API_KEY(self) -> str:
        """Returns the environment variable, ALPHA_API_KEY."""
        return self.flask_app.config.get("ALPHA_API_KEY", UNSET)

    def set_ALPHA_API_KEY(self, new_value: str) -> None:
        """Sets a new value to the environment variable, ALPHA_API_KEY."""
        self.flask_app.config["ALPHA_API_KEY"] = new_value
        
    # GETTER and SETTER methods for the ALLOWED_ORIGINS variable.
    def get_ALLOWED_ORIGINS(self) -> str:
        """Returns the environment variable, ALLOWED_ORIGINS."""
        return self.flask_app.config.get("ALLOWED_ORIGINS", UNSET)

    def set_ALLOWED_ORIGINS(self, new_value: str) -> None:
        """Sets a new value to the environment variable, ALLOWED_ORIGINS."""
        self.flask_app.config["ALLOWED_ORIGINS"] = new_value