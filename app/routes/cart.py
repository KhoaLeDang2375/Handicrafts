from fastapi import APIRouter, HTTPException, Query, Path
from typing import List, Optional
from app.schemas import *
from app.models.product_variant import ProductVariant
from app.models.customer import Customer
from app.models.cart import Cart
from app.security import verify_access_token
router = APIRouter(
    prefix="/my-cart",
    tags=["my-cart"]
)
# Endpoint lấy giỏ hàng của khách hàng
@router.get("/", response_model=CartResponse)
async def get_my_cart(access_token: str = Query(..., description="JWT access token để xác thực người dùng")):
    """Lấy giỏ hàng của khách hàng hiện tại."""
    # Xác thực token và lấy thông tin khách hàng
    try:
        payload = verify_access_token(access_token)
        customer_id = payload.get("sub")
        if customer_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        if payload.get("role") != "customer":
            raise HTTPException(status_code=401, detail="Unauthorized role")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token") from e

    customer = Customer.get_by_id(customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    items_raw = Cart.get_user_cart(customer_id)

    items = []
    for item in items_raw:
        items.append({
            "id": item["id"],
            "user_id": item["user_id"],
            "product_id": item.get("productvariant_id"),   # ánh xạ thủ công
            "productvariant_id": item["productvariant_id"],
            "product_quantity": item["quantity"],          # ánh xạ thủ công
            "total_price": item["total_price"],
            "color": item.get("color"),
            "size": item.get("size"),
            "price": item.get("price"),
            "product_name": item.get("product_name"),
        })

    return CartResponse(
        customer_id=customer_id,
        items=items,
        total_amount=sum(item["total_price"] for item in items)
    )
# Endpoint thêm sản phẩm vào giỏ hàng
@router.post("/add-item", response_model=CartItemAddResponse)
async def add_item_to_cart(cart_item: CartItemAdd):
    """Thêm sản phẩm vào giỏ hàng của khách hàng."""
    # Xác thực token và lấy thông tin khách hàng
    try:
        payload = verify_access_token(cart_item.access_token)
        customer_id = payload.get("sub")
        if customer_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        if payload.get("role") != "customer":
            raise HTTPException(status_code=401, detail="Unauthorized role")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token") from e

    customer = Customer.get_by_id(customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    cart = Cart.get_user_cart(customer_id)
    if cart is None:
        cart = Cart(customer_id=customer_id, items=[], total_amount=0.0)
        cart.save()

    variant = ProductVariant.get_by_id(cart_item.productvariant_id)
    if variant is None:
        raise HTTPException(status_code=404, detail="Product variant not found")

    cart = Cart(user_id=customer_id, productvariant_id=cart_item.productvariant_id, quantity=cart_item.product_quantity)
    cart.save()
    return CartItemAddResponse(
        productvariant_id=cart_item.productvariant_id,
        quantity=cart_item.product_quantity,
        total_price=cart.total_price,
        message="Item added to cart successfully"
    )

# Endpoint xóa sản phẩm khỏi giỏ hàng
@router.delete("/remove-item/{variant_id}", response_model=CartItemDeleteResponse)
async def remove_item_from_cart(
    variant_id: int = Path(..., description="ID của biến thể sản phẩm cần xóa khỏi giỏ hàng"),
    access_token: str = Query(..., description="JWT access token để xác thực người dùng")
):
    """Xóa sản phẩm khỏi giỏ hàng của khách hàng."""
    # Xác thực token và lấy thông tin khách hàng
    try:
        payload = verify_access_token(access_token)
        customer_id = payload.get("sub")
        if customer_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        if payload.get("role") != "customer":
            raise HTTPException(status_code=401, detail="Unauthorized role")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token") from e

    customer = Customer.get_by_id(customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    cart = Cart.get_user_cart(customer_id)
    if cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")

    for item in cart:
        if item['productvariant_id'] == variant_id:
            Cart.remove_item(item['productvariant_id'])
            break
    return CartItemDeleteResponse(   
        productvariant_id=variant_id,
        message="Item removed from cart successfully"
    )
# Endpoint cập nhật số lượng sản phẩm trong giỏ hàng
@router.put("/update-item", response_model=CartItemUpdateResponse)
async def update_item_in_cart(cart_item_update: CartItemUpdate):
    """Cập nhật số lượng sản phẩm trong giỏ hàng của khách hàng."""
    # Xác thực token và lấy thông tin khách hàng
    try:
        payload = verify_access_token(cart_item_update.access_token)
        customer_id = payload.get("sub")
        if customer_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        if payload.get("role") != "customer":
            raise HTTPException(status_code=401, detail="Unauthorized role")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token") from e

    customer = Customer.get_by_id(customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    variant = ProductVariant.get_by_id(cart_item_update.productvariant_id)
    if variant is None:
        raise HTTPException(status_code=404, detail="Product variant not found")
    try:
        Cart.update_item_quantity(
            user_id=customer_id,
            variant_id=cart_item_update.productvariant_id,
            quantity=cart_item_update.product_quantity
        )
        return CartItemUpdateResponse(
            productvariant_id=cart_item_update.productvariant_id,
            quantity=cart_item_update.product_quantity,
            total_price=Cart.get_item(customer_id, cart_item_update.productvariant_id)['total_price'],
            message="Cart item updated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to update cart item") from e