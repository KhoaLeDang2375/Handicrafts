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

class ProductVariantResponse(ProductVariantBase):
    id: int
    product_id: int

class CategoryBase(BaseModel):
    id: int
    name: str

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    category_id: int
    status: str = "In stock"
    artisan_description: str
    variants: List[ProductVariantBase]

class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    category_id: int
    status: str
    artisan_description: str
    category: Optional[CategoryBase] = None
    variants: Optional[List[ProductVariantResponse]] = None

class ProductListItem(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    category_id: int
    status: str
    artisan_description: str
    category_name: Optional[str] = None
    variants: Optional[List[ProductVariantResponse]] = None

class PaginatedProductList(BaseModel):
    items: List[ProductListItem]
    total: int
    skip: int
    limit: int

@router.get("/", response_model=PaginatedProductList)
async def get_products(
    category_id: Optional[int] = Query(None, description="Filter products by category"),
    status: Optional[str] = Query(None, description="Filter products by status"),
    include_variants: bool = Query(False, description="Include product variants in response"),
    skip: int = Query(0, ge=0, description="Skip records"),
    limit: int = Query(10, ge=1, le=100, description="Limit records per page")
):
    """Lấy danh sách sản phẩm với các tùy chọn lọc và phân trang"""
    try:
        if status and status.lower() not in ["in stock", "out of stock"]:
            raise HTTPException(status_code=400, detail="Invalid status value")

        # Get products based on category
        if category_id:
            products = Product.get_by_category(category_id, skip, limit)
            total = Product.count_by_category(category_id)
        else:
            products = Product.get_all(skip, limit)
            total = Product.count_all()

        # Filter by status if specified
        if status:
            products = [p for p in products if p['status'].lower() == status.lower()]
            if category_id:
                total = len(products)  # Recount after filtering

        # Include variants if requested
        if include_variants:
            for product in products:
                variants = ProductVariant.get_by_product(product['id'])
                product['variants'] = variants or []

        return {
            "items": products,
            "total": total,
            "skip": skip,
            "limit": limit
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/category/{category_id}", response_model=PaginatedProductList)
async def get_products_by_category(
    category_id: int = Path(..., description="The ID of the category to filter by"),
    include_variants: bool = Query(False, description="Include product variants in response"),
    skip: int = Query(0, ge=0, description="Skip records"),
    limit: int = Query(10, ge=1, le=100, description="Limit records per page")
):
    """Lấy danh sách sản phẩm theo category"""
    try:
        products = Product.get_by_category(category_id, skip, limit)
        if not products:
            return {
                "items": [],
                "total": 0,
                "skip": skip,
                "limit": limit
            }

        total = Product.count_by_category(category_id)

        if include_variants:
            for product in products:
                variants = ProductVariant.get_by_product(product['id'])
                product['variants'] = variants or []

        return {
            "items": products,
            "total": total,
            "skip": skip,
            "limit": limit
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int = Path(..., description="The ID of the product to get"),
    include_variants: bool = Query(True, description="Include product variants in response")
):
    """Lấy thông tin chi tiết một sản phẩm và các biến thể của nó"""
    try:
        product = Product.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        # Lấy thông tin variants nếu được yêu cầu
        if include_variants:
            variants = ProductVariant.get_by_product(product_id)
            product['variants'] = variants or []

        return product
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=ProductResponse)
async def create_product(product: ProductCreate):
    """Tạo sản phẩm mới với các biến thể"""
    try:
        # Tạo sản phẩm
        new_product = Product(
            name=product.name,
            description=product.description,
            category_id=product.category_id,
            status=product.status,
            artisan_description=product.artisan_description
        )
        product_id = new_product.save()

        # Tạo các biến thể
        variants = []
        for variant in product.variants:
            new_variant = ProductVariant(
                product_id=product_id,
                color=variant.color,
                size=variant.size,
                price=variant.price,
                amount=variant.amount
            )
            variant_id = new_variant.save()
            variants.append({**variant.dict(), 'id': variant_id, 'product_id': product_id})

        # Lấy thông tin sản phẩm vừa tạo
        created_product = Product.get_by_id(product_id)
        created_product['variants'] = variants

        return created_product
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

@router.get("/{product_id}/variants", response_model=List[ProductVariantResponse])
async def get_product_variants(
    product_id: int = Path(..., description="The ID of the product to get variants for")
):
    """Lấy danh sách các biến thể của một sản phẩm"""
    try:
        # Kiểm tra sản phẩm tồn tại
        product = Product.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        variants = ProductVariant.get_by_product(product_id)
        if not variants:
            return []  # Trả về list rỗng thay vì báo lỗi
            
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
