from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class ExceptionMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            print(f"Erro inesperado: {e}")
            return JSONResponse(
                status_code=500,
                content={
                    "status": "error",
                    "message": "Ocorreu um erro interno no servidor.",
                    "details": str(e)
                }
            )
