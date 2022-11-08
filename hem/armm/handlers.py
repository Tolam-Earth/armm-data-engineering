from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


# https://github.com/objectcomputing/hem-architecture/blob/main/armm/information/api/response-codes.md
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({
            "error": {
                "message": "Unprocessable Entity",
                "code": 1006,
                "detail": exc.errors(),
                "request_body": exc.body,
            }
        }),
    )
