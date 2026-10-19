import io
import pandas as pd
import numpy as np
from config import Config

def csv_to_bytes(content: bytes) -> tuple:
    """Read raw CSV bytes into a pandas dataframe
    why bytes instead of a file object
    FastAPI gives bytes from UploadFile.read()
    io.BytesIO wraps those bytes into a file-like object
    that pd.read_csv() can consume — no temp file needed."""

    try:
        df = pd.read_csv(io.BytesIO(content))
    except pd.errors.EmptyDataError:
        return False, "CSV file has no data at all", None
    except pd.errors.ParserError:
        return False, "CSV file is malformed and could not be parsed", None
    except Exception as e:
        return False,f"Could not read CSV: {str(e)}", None

    return True, None, df

def clean_data_frame(df: pd.DataFrame) -> pd.DataFrame:
    """ clean the pandas dataframe to make it safe for JSON conversion
    cleaning invloves
    1. pandas NaN to JSON None for consistency acros frontend
    2. standarize the column name before applying any business logic
    """
    # Nan to None
    df = df.replace({np.nan: None})

    # standarize the column name
    df.columns = [
        col.strip().lower().replace(' ','_').replace('-','_') for col in df.columns
    ]

    return df
def dataframe_to_records(df: pd.DataFrame) -> list:
    """Convert dataframe to a list of dictionaries
     orient='records' → [{col: val, col: val}, {col: val, col: val}]
    This is the shape frontend developers expect for tables and lists."""

    return df.to_dict(orient='records')

def convert_to_json(content: bytes) -> tuple:
    """
    Full pipeline: CSV bytes → cleaned → structured result dict.
    Returns: (success: bool, error_message: str or None, result: dict or None)
    """

    success, error_message, df = csv_to_bytes(content)

    if not success:
        return False, error_message, None
    #If dataframe is empty (headers only, no rows)
    if df.empty:
        return False, "CSV contains headers but no data rows", None
    #Clean the dataframe
    df = clean_data_frame(df)

    # cap rows for maximum allowed rows i.e. 1000
    total_rows = len(df)
    if total_rows > Config.MAX_ROWS_RETURNED:
        df = df.head(Config.MAX_ROWS_RETURNED)
    # dataframe conversion to list of dictionaries
    records = dataframe_to_records(df)

    result = {
        "row_count": len(records),
        "total_rows_in_file": total_rows,
        "columns": list(df.columns),
        "records": records
    }

    return True, None, result

