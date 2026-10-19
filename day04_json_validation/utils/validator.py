from pydantic import ValidationError
from schemas.product import ProductSchema

def validate_records(records: list) -> tuple:
    """validate a list of raw dicts against ProductSchema
    For each record try to create product schema instance
    if it succeeds -> valid
    if it fails(ValidatorError) -> Extract all error messages
    Returns: Valid and Invalid record lists seprately
    """
    valid_records = []
    invalid_records = []

    for record in records:
        try:
            # Attempt validation-raises validation error if any rule fails
            validated = ProductSchema(**record) #upacks the dict into keyword args (id=1, name="Laptop")
            #model_dump() convert back to dict with clean records
            valid_records.append(validated.model_dump())
        except ValidationError as e:
            #Extract all human readale error messages
            errors = [
                f"{err['loc'][0]} : {err['msg']}" for err in e.errors()
            ]
            invalid_records.append({
                "record": record,
                "errors": errors
            })


        except Exception:
            # record is maformed so it can not be unpacked
            invalid_records.append({
                "record" : record,
                "errors": ["Record structure is invalid and could not be processed"]
            })
    return valid_records, invalid_records
