from fastapi import APIRouter, HTTPException, Query, Path
from typing import List, Optional
from pydantic import BaseModel
from app.models.product import Product
from app.models.product_variant import ProductVariant

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

# Pydantic models
class ProductVariantBase(BaseModel):
    color: str
    size: int
    price: float
    amount: int

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    category_id: int
    status: str = "In stock"
    artisan_description: str
    variants: List[ProductVariantBase]

class ProductResponse(BaseModel):
    name: str
    description: Optional[str] = None
    status: str
    artisan_description: Optional[str] = None
    category_name: Optional[str] = None

@router.get("/", response_model=List[ProductResponse])
async def get_products(
    category_id: Optional[int] = Query(None, description="Filter products by category"),
    status: Optional[str] = Query(None, description="Filter products by status")
):
    """Lấy danh sách tất cả sản phẩm"""
    try:
        if category_id:
            products = Product.get_by_category(category_id)
        else:
            products = Product.get_all()
        
        if status:
            products = [p for p in products if p['status'] == status]
            
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int = Path(..., description="The ID of the product to get")
):
    """Lấy thông tin một sản phẩm cụ thể"""
    try:
        product = Product.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=dict)
async def create_product(product: ProductCreate):
    """Tạo sản phẩm mới"""
    try:
        # Create product
        new_product = Product(
            name=product.name,
            description=product.description,
            category_id=product.category_id,
            status=product.status,
            artisan_description=product.artisan_description
        )
        product_id = new_product.save()

        # Create variants
        for variant in product.variants:
            new_variant = ProductVariant(
                product_id=product_id,
                color=variant.color,
                size=variant.size,
                price=variant.price,
                amount=variant.amount
            )
            new_variant.save()

        return {
            "status": "success",
            "message": "Product created successfully",
            "product_id": product_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{product_id}/status")
async def update_product_status(
    product_id: int,
    status: str = Query(..., description="New status for the product")
):
    """Cập nhật trạng thái sản phẩm"""
    try:
        if status not in ["In stock", "out of stock"]:
            raise HTTPException(status_code=400, detail="Invalid status")
        
        success = Product.update_status(product_id, status)
        if not success:
            raise HTTPException(status_code=404, detail="Product not found")
            
        return {"message": f"Product status updated to {status}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{product_id}/variants")
async def get_product_variants(product_id: int):
    """Lấy danh sách variant của sản phẩm"""
    try:
        variants = ProductVariant.get_by_product(product_id)
        if not variants:
            raise HTTPException(status_code=404, detail="No variants found for this product")
        return variants
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/variants/{variant_id}/stock")
async def update_variant_stock(
    variant_id: int,
    amount: int = Query(..., description="Amount to add (positive) or subtract (negative)")
):
    """Cập nhật số lượng tồn kho của variant"""
    try:
        variant = ProductVariant.get_by_id(variant_id)
        if not variant:
            raise HTTPException(status_code=404, detail="Variant not found")
            
        new_amount = variant['amount'] + amount
        if new_amount < 0:
            raise HTTPException(status_code=400, detail="Insufficient stock")
            
        success = ProductVariant().update_stock(variant_id, amount)
        if success:
            return {"message": f"Stock updated successfully. New amount: {new_amount}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))