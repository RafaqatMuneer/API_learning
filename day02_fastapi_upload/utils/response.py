from typing import Optional, Any
from pydantic import BaseModel
from datetime import datetime, timezone

# ─── Pydantic Response Models ────────────────────

class SuccessResponse(BaseModel):
    """Standard response for success, 
    pydantic validated the every field match its type"""
    status: str = "success"
    message: str = "Success"
    data: Optional[Any] = None
    timestamp : str = ""

    def model_post_init(self, __context:Any) -> None:
        "Timetsamp with every response"
        self.timestamp = datetime.now(timezone.utc).isoformat()

class ErrorResponse(BaseModel):
    """Standard response for error, 
    pydantic validated the every field match its type"""
    status: str = "error"
    message: str = "Something went wrong"
    data: None = None
    timestamp : str = ""

    def model_post_init(self, __context:Any) -> None:
        "Timetsamp with every response"
        self.timestamp = datetime.now(timezone.utc).isoformat()

# ─── Builder or Helper Functions ─────────────────────────────
def success_response(
        data : Any = None,
        message : str = "Success",
        status_code : int = 200 
        ) -> tuple:
    "Build a standard success response tuple (body, status_code)."
    return SuccessResponse(message=message, data=data), status_code

def error_response(
        message : str = "Something went wrong",
        status_code : int = 400
        ) -> tuple:
    "Build a standard error response tuple (body, status_code)."
    return ErrorResponse(message=message), status_code
    







# response = ErrorResponse(
#     message = "User not created",
# )

# print(response.model_dump())