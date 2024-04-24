"""
Schema related utility functions, classes, constants, etc.
"""
from flask_restx import fields as flask_restx_fields, Model as ApiModel
from marshmallow import Schema, EXCLUDE, missing, fields as marshmallow_fields


class _FieldDefinition:
    """Creating a custom class for defining a field."""
    def __init__(self, name: str, value: any):
        self.name = name
        self.value = value


class BaseFields:
    """This defines the common fields that are used in all."""
    createdTimestamp = _FieldDefinition(
        name="createdTimestamp",
        value=marshmallow_fields.DateTime(
            required=False,  # for creation
            default=None,
            allow_none=True,
            metadata={
                'description': "A timestamp for when the document was created.",
                'readonly': True
            }
        )
    )
    modifiedTimestamp = _FieldDefinition(
        name="modifiedTimestamp",
        value=marshmallow_fields.DateTime(
            required=False,  # for creation
            default=None,
            allow_none=True,
            metadata={
                'description': "A timestamp for when the last time this document was modified, or updated.",
                'readonly': True
            }
        )
    )
    active = _FieldDefinition(
        name="active",
        value=marshmallow_fields.Boolean(
            required=False,  # for creation
            default=True,
            allow_none=True,
            metadata={
                'description': "Is this document active or not?",
                'readonly': True
            }
        )
    )
    ALL = [createdTimestamp, modifiedTimestamp, active]


class BaseSchema(Schema):
    """
    This is the base Schema class that all other Schema classes should inherit 
    from.
    """
    class Meta:
        unknown = EXCLUDE
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in BaseFields.ALL:
            field_name = field.name
            field_value = field.value
            self.fields.update({field_name:field_value})
            self.load_fields.update({field_name:field_value})
            self.dump_fields.update({field_name:field_value})


def create_api_model_from_schema(schema_cls: Schema, api_model_name: str) -> ApiModel:
    """Creates a Flask RestX API Model object from a marshmallow Schema class.
    
    Extracts the attributes and types declared in the provided marshmallow 
    Schema class and creates a new Flask RestX API Model object.
    
    Args:
        schema_cls: (marshmallow.Schema) The marshmallow Schema class to convert 
            into a Flask RestX API Model.
        api_model_name: (str) The name to associate to the API Model.
            
    Returns:
        A new flask_restx.Model object.
    """
    type_class_mappings = {
        # marshmallow field type -> flask_restx field type
        marshmallow_fields.String: flask_restx_fields.String,
        marshmallow_fields.Number: flask_restx_fields.Integer,
        marshmallow_fields.DateTime: flask_restx_fields.DateTime,
        marshmallow_fields.Boolean: flask_restx_fields.Boolean,
        marshmallow_fields.AwareDateTime: flask_restx_fields.DateTime,
        marshmallow_fields.NaiveDateTime: flask_restx_fields.DateTime,
        marshmallow_fields.List: flask_restx_fields.List
        # CustomDateTime: flask_restx_fields.DateTime
    }
    new_schema_dict = dict()
    for attr, field in schema_cls().fields.items():
        field_details = vars(field)
        try: 
            flask_restx_field_cls = type_class_mappings[type(field)]
        except Exception: 
            flask_restx_field_cls = flask_restx_fields.String      # default to string
        if flask_restx_field_cls == flask_restx_fields.List:
            metadata = field_details.get('metadata')
            inner_schema = metadata.get('inner_schema', [])
            new_schema_dict[attr] = flask_restx_fields.Raw(
                default=inner_schema,
                attribute=field_details.get('attribute') if field_details.get('attribute') != missing else None,
                title=attr,
                description=field_details.get('metadata').get('description'),
                required=field_details.get('required') if field_details.get('required') != missing else None,
                readonly=field_details.get('metadata').get('readonly')
            )
        else:
            new_schema_dict[attr] = flask_restx_field_cls(
                default=field_details.get('dump_default') if field_details.get('dump_default') != missing else None,
                attribute=field_details.get('attribute') if field_details.get('attribute') != missing else None,
                title=attr,
                description=field_details.get('metadata').get('description'),
                required=field_details.get('required') if field_details.get('required') != missing else None,
                readonly=field_details.get('metadata').get('readonly')
            )
    return ApiModel(api_model_name, new_schema_dict)