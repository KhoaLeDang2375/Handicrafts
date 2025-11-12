from fastapi import APIRouter, HTTPException, Query, Path
from typing import List, Optional
from app.models import shipment
from app.schemas import *
import json
from app.models.cart import Cart
from app.models.order import Order
from app.models.order_detail import OrderDetail
from app.models.product_variant import ProductVariant
from app.models.customer import Customer
from app.models.employee import Employee
from app.models.payment import Payment
from app.models.shipment import Shipment
from datetime import datetime
from app.security import verify_access_token
from app.database import db
router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)
# Endpoint mua một sản phẩm ngay (buy-now)
@router.post("/buy-now", response_model=OrderCheckoutResponse)
async def buy_now(order_data: OrderCheckoutOne):
    """Mua ngay 1 sản phẩm (không thay đổi giỏ hàng)."""
    # Xác thực token và lấy thông tin khách hàng
    try:
        payload = verify_access_token(order_data.access_token)
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

    try:
        db.begin_transaction()

        new_order = Order(user_id=customer_id, total_amount=0.0, status="processing")
        new_order.save()

        item = order_data.item
        variant = ProductVariant.get_by_id(item.productvariant_id)
        if variant is None:
            raise HTTPException(status_code=404, detail="Product variant not found")

        item_price = variant['price'] if isinstance(variant, dict) else variant.price
        item_total = item_price * item.product_quantity

        order_detail = OrderDetail(
            order_id=new_order.id,
            variant_id=item.productvariant_id,
            product_quantity=item.product_quantity,
            price=item_price
        )
        order_detail.save()

        # Cập nhật tổng tiền
        update_query = """UPDATE Orders SET total_amount = %s WHERE id = %s"""
        db.execute_query(update_query, (item_total, new_order.id))

        db.commit_transaction()

        return OrderCheckoutResponse(message="Order created successfully", order_id=new_order.id)

    except HTTPException:
        try:
            db.rollback_transaction()
        except Exception:
            pass
        raise
    except Exception as e:
        try:
            db.rollback_transaction()
        except Exception:
            pass
        raise HTTPException(status_code=500, detail=f"Failed to create order: {e}")


# Endpoint checkout từ giỏ hàng (mua nhiều sản phẩm)
@router.post("/checkout", response_model=OrderCheckoutResponse)
async def checkout(order_data: OrderCheckout):
    """Tạo đơn hàng từ danh sách sản phẩm (cart_items). Sau khi mua sẽ xóa giỏ hàng."""
    # Xác thực token và lấy thông tin khách hàng
    try:
        payload = verify_access_token(order_data.access_token)
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

    try:
        db.begin_transaction()

        new_order = Order(user_id=customer_id, total_amount=0.0, status="processing")
        new_order.save()

        total_amount = 0.0
        for item in order_data.cart_items:
            variant = ProductVariant.get_by_id(item.productvariant_id)
            if variant is None:
                raise HTTPException(status_code=404, detail="Product variant not found")
            price = variant['price'] if isinstance(variant, dict) else variant.price
            item_total = price * item.product_quantity
            total_amount += item_total

            order_detail = OrderDetail(
                order_id=new_order.id,
                variant_id=item.productvariant_id,
                product_quantity=item.product_quantity,
                price=price
            )
            order_detail.save()
        # Thêm thông tin giao hàng và thanh toán 
        payment = Payment(
            payment_method=order_data.payment_method,
            status="pending",
            payment_date = None
        )
        payment.save()
        shipment = Shipment(
            order_id=new_order.id,
            carrier=order_data.shipment,
            status= "pending"
        )
        shipment.save()
        # Cập nhật tổng tiền
        update_query = """UPDATE orders SET total_amount = %s WHERE id = %s"""
        db.execute_query(update_query, (total_amount, new_order.id))

        db.commit_transaction()

        # Clear product bought user's cart after successful purchase
        try:
            for item in order_data.cart_items:
                Cart.remove_item(customer_id, item.productvariant_id)
        except Exception:
            # non-fatal: cart cleanup failed but order succeeded
            pass

        return OrderCheckoutResponse(message="Order created successfully", order_id=new_order.id)

    except HTTPException:
        try:
            db.rollback_transaction()
        except Exception:
            pass
        raise
    except Exception as e:
        try:
            db.rollback_transaction()
        except Exception:
            pass
        raise HTTPException(status_code=500, detail=f"Failed to create order: {e}")
# Các router xem đơn hàng của khách hàng
@router.get("/my-orders", response_model=List[OrderCheckResponse])
def get_my_orders(check_data: OrderCheckRequest):
    # Logic để lấy đơn hàng của khách hàng
    # Xác thực khách hàng
    try:
        payload = verify_access_token(check_data.access_token)
        customer_id = payload.get("sub")
        if customer_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        if payload.get("role") != "customer":
            raise HTTPException(status_code=401, detail="Unauthorized role")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token") from e
    # Lấy đơn hàng của khách hàng
    orders = Order.get_user_orders(customer_id)
    # Lọc theo trạng thái nếu được cung cấp
    if check_data.status:
        orders = [order for order in orders if order['status'] == check_data.status]
    # Trả về danh sách đơn hàng
    response = []
    for order in orders:
        response.append(OrderCheckResponse(
            order_id=order['id'],
            user_id=order['user_id'],
            total_amount=order['total_amount'],
            status=order['status'],
            created_at=order['created_at'],
            updated_at=order['updated_at']
        ))
    return response
# Router để update các đơn hàng (dành cho các đơn hàng đang processing)
