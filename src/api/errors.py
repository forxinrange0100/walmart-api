from fastapi import Request
from fastapi.responses import JSONResponse
class AppError(Exception):
    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(detail)

class NotFoundDataError(AppError):
    pass

class InvalidDataError(AppError):
    pass
async def handle_not_found_error(request: Request, exc: NotFoundDataError):
    print(f"Not found: {exc.detail}")
    return JSONResponse(status_code=404, content={"message": exc.detail})

async def handle_invalid_data_error(request: Request, exc: InvalidDataError):
    print(f"Invalid data: {exc.detail}")
    return JSONResponse(status_code=400, content={"message": exc.detail})

async def handle_internal_error(request: Request, exc: Exception):
    print(f"Internal error: {str(exc)}")
    return JSONResponse(status_code=500, content={"message": "Internal server error"})