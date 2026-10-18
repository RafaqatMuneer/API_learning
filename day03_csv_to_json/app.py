from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from utils.response import error_response
from config import Config
from routes.health import router as health_router
from routes.products import router as products_router
from routes.uploads import router as uploads_router


def create_app() -> FastAPI:
    app = FastAPI(
        title=Config.APP_NAME,
        version=Config.VERSION,
        docs_url="/docs", # Swagger UI — free with FastAPI
        redoc_url="/redoc"       # Alternative docs UI
    )
    app.include_router(health_router, prefix=Config.API_PREFIX)
    app.include_router(products_router, prefix=Config.API_PREFIX)
    app.include_router(uploads_router, prefix=f"{Config.API_PREFIX}/uploads")

    # Global 404 Handler
    @app.exception_handler(404)
    async def not_found(request: Request, exc):
        body, status_code = error_response(
            message="The route you are looking for does not exist",
            status_code=404
        )
        return JSONResponse(content=body.model_dump(), status_code=status_code)
    # Global 405 handler
    @app.exception_handler(405)
    async def method_not_allowed(request: Request, exc):
        body, status_code = error_response(
            message="HTTP method not allowed on this route",
            status_code=405
        )
        return JSONResponse(content=body.model_dump(), status_code=status_code)

    # Global 422 handler — FastAPI's validation error
    @app.exception_handler(422)
    async def validation_error(request: Request, exc):
        body, status_code = error_response(
            message="Invalid input — please check your request parameters",
            status_code=422
        )
        return JSONResponse(content=body.model_dump(), status_code=status_code)

    return app

app = create_app()


