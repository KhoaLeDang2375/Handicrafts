from fastapi import APIRouter, HTTPException, Query, Path
from typing import List, Optional
from app.schemas import *
import json
from app.models.product import Product
from app.models.product_variant import ProductVariant
from app.security import verify_access_token
router = APIRouter(
    prefix="/products",
    tags=["products"]
)

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

        # Parse category JSON returned by MySQL JSON_OBJECT (may come as string)
        if 'category' in product and isinstance(product['category'], str):
            try:
                product['category'] = json.loads(product['category'])
            except Exception:
                # leave as-is if parsing fails
                pass

        return product
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=ProductResponse)
async def create_product(product: ProductCreate):
    """Tạo sản phẩm mới với các biến thể"""
    try:
        # Tạo sản phẩm
        # Kiểm tra chỉ employee mới được tạo sản phẩm
        user = verify_access_token(product.access_token)
        if user['role'] != 'employee':
            raise HTTPException(status_code=403, detail="Only employees can create products")

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

@router.get("/variant/{product_id}/variants", response_model=List[ProductVariantResponse])
async def get_product_variants(
    product_id: int = Path(..., description="The ID of the product to get variants for")
):
    """Lấy danh sách các biến thể của một sản phẩm"""
    try:
        # Kiểm tra sản phẩm tồn tại
        product = Product.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        variants = ProductVariant.get_by_product(product_id, variant_id = None, get_one= False)
        if not variants:
            return []  # Trả về list rỗng thay vì báo lỗi
            
        return variants
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# Lấy endpoint lấy một biến thể của sản phẩm
@router.get("/{product_id}/variants/{variant_id}", response_model=ProductVariantResponse)
async def get_product_variant_one(
    product_id: int = Path(..., description="The ID of the product"),
    variant_id: int = Path(..., description="The ID of the variant")
):
    try:
        product = Product.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        variant = ProductVariant.get_by_product(product_id=product_id, variant_id=variant_id, get_one=True)
        if not variant:
            raise HTTPException(status_code=404, detail="Variant not found")

        return variant
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/variant/{product_variant_id}", response_model=ProductVariantUpdateResponse)
async def update_product_variant(product_variant_id: int, update_data: UpdateBase):
    """Cập nhật thông tin một biến thể sản phẩm"""
    try:
        # Xác thực token và kiểm tra quyền employee
        payload = verify_access_token(update_data.access_token)
        if payload.get("role") != "employee":
            raise HTTPException(status_code=403, detail="Only employees can update product variants")

        # Lấy biến thể sản phẩm hiện tại
        variant = ProductVariant.get_by_id(product_variant_id)
        if not variant:
            raise HTTPException(status_code=404, detail="Product variant not found")

        # Cập nhật các trường nếu được cung cấp
        update_fields = {}
        for field in ['name', 'description', 'artisan_description', 'status', 'category_id', 'color', 'size', 'price', 'amount']:
            value = getattr(update_data, field)
            if value is not None:
                update_fields[field] = value

        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields provided for update")

        success = ProductVariant.update(product_variant_id, **update_fields)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update product variant")

        updated_variant = ProductVariant.get_by_id(product_variant_id)
        return {
            "id": updated_variant['id'],
            "product_id": updated_variant['product_id'],
            "message": "Product variant updated successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# Delete product endpoint
@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    access_token: str = Query(..., description="JWT access token to authenticate the user")
):
    """Xóa một sản phẩm và tất cả biến thể của nó"""
    try:
        # Xác thực token và kiểm tra quyền employee
        payload = verify_access_token(access_token)
        if payload.get("role") != "employee":
            raise HTTPException(status_code=403, detail="Only employees can delete products")

        # Kiểm tra sản phẩm tồn tại
        product = Product.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        # Xóa sản phẩm và các biến thể liên quan
        success = Product.delete(product_id)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete product")

        return {"message": "Product and its variants deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# Delete product variant endpoint
@router.delete("/variants/{variant_id}")
async def delete_product_variant(
    variant_id: int,
    access_token: str = Query(..., description="JWT access token to authenticate the user")
):
    """Xóa một biến thể sản phẩm"""
    try:
        # Xác thực token và kiểm tra quyền employee
        payload = verify_access_token(access_token)
        if payload.get("role") != "employee":
            raise HTTPException(status_code=403, detail="Only employees can delete product variants")

        # Kiểm tra biến thể sản phẩm tồn tại
        variant = ProductVariant.get_by_id(variant_id)
        if not variant:
            raise HTTPException(status_code=404, detail="Product variant not found")

        # Xóa biến thể sản phẩm
        success = ProductVariant.delete(variant_id)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete product variant")

        return {"message": "Product variant deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))