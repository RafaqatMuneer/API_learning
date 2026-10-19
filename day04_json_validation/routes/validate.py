from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Any
from utils.response import success_response, error_response
from utils.validator import validate_records

router = APIRouter()

class ValidationRequest(BaseModel):
    """Defines the expected shape of request body.
    FASTAPI reads this type hint validates the incoming 
    JSON body autmoatically-before function runs"""
    records: list[Any]

@router.post("/json")
async def validate_json(payload:ValidationRequest):
    """Recieve a list of product records, validate each product
    against product schema and return either valid or invalid for each record"""
    # Check: is the records list empty
    if not payload.records:
        body, status_code = error_response(
            message="No records provided for validation",
            status_code=400
        )
        return JSONResponse(content=body.model_dump(), status_code=status_code)
    
    # Run validation pipline
    valid_records, invalid_records = validate_records(payload.records)

    #Build Summary
    result = {
        "summary" : {
            "total": len(payload.records),
            "valid": len(valid_records),
            "invalid": len(invalid_records)
        },
        "valid_records": valid_records,
        "invalid_records": invalid_records
    }

    body, status_code = success_response(
        data=result,
        message="Validation complete"
    )
    return JSONResponse(content=body.model_dump(), status_code=status_code)

