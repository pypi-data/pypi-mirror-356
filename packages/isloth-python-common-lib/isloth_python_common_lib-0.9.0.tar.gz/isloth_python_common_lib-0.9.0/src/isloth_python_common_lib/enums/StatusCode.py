"""
StatusCode.py
-------------
Defines standardized HTTP status codes used across iSloth backend services.
"""

from enum import IntEnum


class StatusCode(IntEnum):
    """
    Enum representing HTTP status codes used for API responses.

    Attributes
    ----------
    Success (2xx)
    --------------------
    OK : int
        200 - Standard response for successful GET, PUT, or DELETE.
    CREATED : int
        201 - New resource created, typically after POST.
    ACCEPTED : int
        202 - Request accepted for async processing.
    NON_AUTHORITATIVE_INFORMATION : int
        203 - Metadata from external source.
    NO_CONTENT : int
        204 - No content to return; success without body.

    Client Errors (4xx)
    --------------------
    BAD_REQUEST : int
        400 - Malformed input or missing fields.
    UNAUTHORIZED : int
        401 - Authentication required.
    PAYMENT_REQUIRED : int
        402 - Reserved; optionally for payment failure.
    FORBIDDEN : int
        403 - Authenticated but not permitted.
    NOT_FOUND : int
        404 - Resource not found.
    METHOD_NOT_ALLOWED : int
        405 - Method not supported by endpoint.
    NOT_ACCEPTABLE : int
        406 - Content negotiation failed.
    REQUEST_TIMEOUT : int
        408 - Request took too long.
    CONFLICT : int
        409 - Duplicate or conflicting request.
    LENGTH_REQUIRED : int
        411 - Content-Length header required.
    PRECONDITION_FAILED : int
        412 - Failed precondition headers.
    PAYLOAD_TOO_LARGE : int
        413 - Request body too large.
    URI_TOO_LONG : int
        414 - Excessive URI length.
    UNSUPPORTED_MEDIA_TYPE : int
        415 - Unsupported Content-Type.
    UNPROCESSABLE_ENTITY : int
        422 - Valid JSON but semantically invalid.
    LOCKED : int
        423 - Resource is locked.
    FAILED_DEPENDENCY : int
        424 - Dependent request failed.
    UPGRADE_REQUIRED : int
        426 - Protocol upgrade required.
    PRECONDITION_REQUIRED : int
        428 - Missing conditional headers.
    TOO_MANY_REQUESTS : int
        429 - Rate limit exceeded.

    Server Errors (5xx)
    --------------------
    INTERNAL_SERVER_ERROR : int
        500 - Generic server failure.
    NOT_IMPLEMENTED : int
        501 - Feature not implemented.
    BAD_GATEWAY : int
        502 - Upstream failure.
    SERVICE_UNAVAILABLE : int
        503 - Server unavailable or overloaded.
    HTTP_VERSION_NOT_SUPPORTED : int
        505 - Unsupported HTTP version.
    INSUFFICIENT_STORAGE : int
        507 - Disk/storage full.
    LOOP_DETECTED : int
        508 - Infinite loop detected in request.
    NETWORK_AUTHENTICATION_REQUIRED : int
        511 - Network authentication needed.
    """

    # 2xx Success
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NON_AUTHORITATIVE_INFORMATION = 203
    NO_CONTENT = 204

    # 4xx Client Errors
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    PAYMENT_REQUIRED = 402
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    NOT_ACCEPTABLE = 406
    REQUEST_TIMEOUT = 408
    CONFLICT = 409
    LENGTH_REQUIRED = 411
    PRECONDITION_FAILED = 412
    PAYLOAD_TOO_LARGE = 413
    URI_TOO_LONG = 414
    UNSUPPORTED_MEDIA_TYPE = 415
    UNPROCESSABLE_ENTITY = 422
    LOCKED = 423
    FAILED_DEPENDENCY = 424
    UPGRADE_REQUIRED = 426
    PRECONDITION_REQUIRED = 428
    TOO_MANY_REQUESTS = 429

    # 5xx Server Errors
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503
    HTTP_VERSION_NOT_SUPPORTED = 505
    INSUFFICIENT_STORAGE = 507
    LOOP_DETECTED = 508
    NETWORK_AUTHENTICATION_REQUIRED = 511
