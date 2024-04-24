"""
File containing API schemas that can be shared across many namespaces.
"""
from flask_restx import Model, fields

from app.constants import (
    EClientErrorMessages,
    EHttpMessages,
)

# from app.firestore.schemas import (
#     BrotherDocumentApiModel,
# )


DEFAULT_MESSAGE_FIELD = fields.String(description="Message describing the outcome of the request.")


"""
API Schemas for default responses.
"""
BasicResponseSchema = Model('BasicResponse', {
    'message': DEFAULT_MESSAGE_FIELD,
    'data': fields.Raw(default={}, description="Contains relevant and detailed data for the request.")
})
BadRequestResponseSchema = Model('BadRequstResponse', {
    'message': fields.String(default=EHttpMessages.BAD_REQUEST),
    'data': fields.String(description="The reason why the request is bad.")
})
UnauthorizedResponseSchema = Model('UnauthorizedResponse', {
    'message': fields.String(default=EHttpMessages.UNAUTHORIZED),
    'data': fields.String(default=EClientErrorMessages.UNAUTHORIZED)
})
InternalServerErrorResponseSchema = Model('InternalServerErrorResponse', {
    'message': fields.String(default=EHttpMessages.INTERNAL_SERVER_ERROR),
    'data': fields.String(default=EClientErrorMessages.INTERNAL_SERVER_ERROR)
})


"""
API Schemas for the 'Brothers' collection.
"""
# BrotherResponseSchema = Model('BrotherResponse', {
#     'message': DEFAULT_MESSAGE_FIELD,
#     'data': fields.Nested(BrotherDocumentApiModel)
# })

"""
Export a list of the schemas we want to register with our API. This is used at 
app start and doing this makes management a bit easier.
"""
SCHEMAS_TO_REGISTER = [
    # General API Response Schemas:
    BasicResponseSchema,
    BadRequestResponseSchema,
    UnauthorizedResponseSchema,
    InternalServerErrorResponseSchema,
    # 'Brothers' collection:
    # BrotherDocumentApiModel,
    # BrotherResponseSchema,
    # BrotherResponseSchema,
]