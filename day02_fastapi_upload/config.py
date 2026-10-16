class Config:
    APP_NAME: str = "AutomatePK API"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    API_PREFIX: str = "/api"
    #Upload Settings
    UPLOAD_FOLDER: str = "uploads"
    MAX_FILE_SIZE_BYTES: int = 2*1024*1024
    ALLOWED_EXTENSIONS: set = {"csv", "json"}