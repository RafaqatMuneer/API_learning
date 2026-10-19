from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from utils.response import success_response, error_response
from utils.file_handler import validate_file, save_file, get_file_extension

router = APIRouter()

@router.post("/file", status_code=201)
async def upload_file(file: UploadFile = File(...)): # the three dots automatically through error if no file selected
    "Accept a upload file, validate it, save it and return metadata"
    # validate file
    is_valid, error_message, content = await validate_file(file)

    if not is_valid:
        body, status_code = error_response(
            message=error_message,
            status_code=400
        )
        return JSONResponse(content=body.model_dump(),status_code=status_code)
    #Save file safely
    save_name, saved_path = await save_file(file, content)

    #prepare metadata
    metadata = {
        "filename" : save_name,
        "size_bytes" : len(content),
        "extension" : get_file_extension(save_name),
        "saved_path": saved_path
    }

    # data against successful response
    body, status_code = success_response(
        data= metadata,
        message="File uploaded successfully",
        status_code=201
    )
    return JSONResponse(content=body.model_dump(), status_code=status_code)