import os
import re
from config import Config

def get_file_extension(filename: str) -> str:
    """
    Extract lower case extension from filename
    """
    return filename.rsplit('.',1)[-1].lower() if '.' in filename else ''

def is_allowed_extension(filename: str) -> bool:
    "Check if the file extension is allowed"
    return get_file_extension(filename) in Config.ALLOWED_EXTENSIONS

def make_safe_filename(filename: str) -> str:
    "Sanitize a filename to prevent path traversal attacks."
    # step 1: strip any path component - take only filename itself
    filename = os.path.basename(filename)

    # replace spaces with underscore
    filename = filename.replace(" ", "_")

    #remove unsafe characters - keep only safe ones
    filename = re.sub(r'[^\w\-_.]', '', filename)

    return filename or "uploaded_file"

async def validate_file(file) -> tuple:
    "performs all validation checks on uploaded file"
    # check is the file have a name
    if not file.filename or file.filename.strip() == "":
        return False,"No File selected", None
    # Check for allowed extension
    if not is_allowed_extension(file.filename):
        allowed = ', '.join(Config.ALLOWED_EXTENSIONS)
        return False,f"File type is not allowed, Allowed types are: {allowed}", None
    # Read content check empty and size
    content = await file.read()
    if len(content) == 0:
        return False, "File is empty", None
    if len(content) > Config.MAX_FILE_SIZE_BYTES:
        max_allowed_mb = Config.MAX_FILE_SIZE_BYTES / (1024*1024)
        return False,f"File too large, Max allowed is {max_allowed_mb:.0f} MB", None

    # Reset file pointer so it can be read again if needed
    await file.seek(0)

    return True, None, content

async def save_file(file, content: bytes) -> tuple:
    "Save validated file to the uploaded folder"
    safe_name = make_safe_filename(file.filename)
    
    save_path = os.path.join(Config.UPLOAD_FOLDER, safe_name)
    # Write bytes directly — no streaming needed at this scale
    with open(save_path, 'wb') as f:
        f.write(content)
    return safe_name, save_path

    


