from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from utils.response import success_response, error_response
from utils.file_handler import validate_file, get_file_extension
from utils.data_converter import convert_to_json

router = APIRouter()

@router.post("/csv-to-json")
async def csv_to_json(file: UploadFile = File(...)):
    """Accept a CSV uploaded file,
    validate it, covert it to JSON
    return structured data"""
    is_valid, error_message, content = await validate_file(file)

    if not is_valid:
        body, status_code = error_response(
            message=error_message,
            status_code=400
        )
        return JSONResponse(content=body.model_dump(), status_code=status_code)
    # this endpoint should accept csv files only
    if get_file_extension(file.filename) != "csv":
        body, status_code = error_response(
            message = "Invalid file type! only .csv files can be uploaded",
            status_code = 400
        )
        return JSONResponse(content=body.model_dump(), status_code= status_code)
    #csv to json file conversion
    success, error_message, result = convert_to_json(content)
    # if conversion fails
    if not success:
        body, status_code = error_response(
            message = error_message,
            status_code = 400
        )
        return JSONResponse(content=body.model_dump(), status_code=status_code)
    body, status_code = success_response(
        data=result,
        message="CSV converted successfully"
    )
    return JSONResponse(content=body.model_dump(), status_code=status_code)

