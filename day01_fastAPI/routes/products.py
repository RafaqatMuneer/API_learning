from fastapi import APIRouter
from fastapi.responses import JSONResponse
from utils.response import success_response, error_response

router = APIRouter()

# Static data
PRODUCTS = [
    {"id": 1, "name": "Laptop",  "price": 85000, "in_stock": True},
    {"id": 2, "name": "Mouse",   "price": 1500,  "in_stock": True},
    {"id": 3, "name": "Monitor", "price": 32000, "in_stock": False}
]

@router.get("/products")
def get_products():
    "Return all products list"
    body, status_code = success_response(
        data=PRODUCTS,
        message="Products fetched successfully"
        )
    return JSONResponse(content=body.model_dump(), status_code=status_code)
@router.get("/product/{product_id}")
def get_product(product_id: int):
    """Return a single product by ID. 
        FastAPI validates this automatically"""
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)

    if product is None:
        body, status_code = error_response(
            message=f"Product with id {product_id} not found",
            status_code=404
        )
        return JSONResponse(content=body.model_dump(), status_code=status_code)
    body, status_code = success_response(
        data = product,
        message="Product Fetched successfully"
    )
    return JSONResponse(content=body.model_dump(),status_code=status_code)

@router.get("/categories")
def get_categories():
    """Return product categories."""
    categories = [
        {"id": 1, "name": "Electronics"},
        {"id": 2, "name": "Clothing"},
        {"id": 3, "name": "Sports"}
    ]
    body, status_code = success_response(
        data=categories,
        message="Categories fetched successfully"
    )
    return JSONResponse(content=body.model_dump(), status_code=status_code)
