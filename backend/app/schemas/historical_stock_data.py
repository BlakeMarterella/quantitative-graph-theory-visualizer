"""
File containing a Schema and API model for the "historical_stock_data" collection.
"""
from marshmallow import fields as marshmallow_fields

from app.schemas.util import (
    BaseSchema, 
    create_api_model_from_schema, 
    _FieldDefinition
)

# Fields
class HistoricalStockDataFields:
    """
    Defining all the User document fields.
    """
    
    ticker = _FieldDefinition(
        name="ticker",
        value=marshmallow_fields.String(
            required=True,
            default="",
            allow_none=True,
            metadata={
                'description': "Ticker for the desired stock."
            }
        )
    )

    start_date = _FieldDefinition(
        name="start_date",
        value=marshmallow_fields.DateTime(
            required=False,
            default=None,
            allow_none=True,
            metadata={
                'description': "The start date of historical stock data range requested"
            }
        )
    )

    end_date = _FieldDefinition(
        name="end_date",
        value=marshmallow_fields.DateTime(
            required=False,
            default=None,
            allow_none=True,
            metadata={
                'description': "The end date of historical stock data range requested"
            }
        )
    )
    
    output_file_type = _FieldDefinition(
        name="output_file_type",
        value=marshmallow_fields.String(
            required=False,
            default="json",
            allow_none=True,
            metadata={
                'description': "The format of the output file. Options: ['json', 'csv']"
            }
        )
    )
    
    
    ALL = [ticker, start_date, end_date, output_file_type]


# Schema
class HistoricalStockDataDocumentSchema(BaseSchema):
    """
    Marshmallow schema for the User document.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in HistoricalStockDataFields.ALL:
            field_name = field.name
            field_value = field.value
            self.fields.update({field_name:field_value})
            self.load_fields.update({field_name:field_value})
            self.dump_fields.update({field_name:field_value})


# API Model
HistoricalStockDataDocumentApiModel = create_api_model_from_schema(
    schema_cls=HistoricalStockDataDocumentSchema,
    api_model_name="HistoricalStockDataDocument"
)