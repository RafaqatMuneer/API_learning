from fastapi import APIRouter
from fastapi.responses import JSONResponse
from utils.response import success_response

router = APIRouter()

@router.get("/health")
async def health_check():
    "App level health check endpoint"
    body, status_code = success_response(message="Server is running")
    return JSONResponse(
        content=body.model_dump(),
        status_code=status_code
    )
