# from fastapi import APIRouter, HTTPException, Query, Path
# from typing import List, Optional
# from app.models import shipment
# from app.schemas import *
# import json
# from app.models.cart import Cart
# from app.models.order import Order
# from app.models.order_detail import OrderDetail
# from app.models.product_variant import ProductVariant
# from app.models.customer import Customer
# from app.models.employee import Employee
# from app.models.payment import Payment
# from app.models.shipment import Shipment
# from datetime import datetime
# from app.security import verify_access_token
# from app.database import db
# router = APIRouter(
#     prefix="/orders",
#     tags=["orders"]
# )
# # Endpoint mua một sản phẩm ngay (buy-now)
# @router.post("/buy-now", response_model=OrderCheckoutResponse)
# async def buy_now(order_data: OrderCheckoutOne):
#     """Mua ngay 1 sản phẩm (không thay đổi giỏ hàng)."""
#     # Xác thực token và lấy thông tin khách hàng
#     try:
#         payload = verify_access_token(order_data.access_token)
#         customer_id = payload.get("sub")
#         if customer_id is None:
#             raise HTTPException(status_code=401, detail="Invalid token payload")
#         if payload.get("role") != "customer":
#             raise HTTPException(status_code=401, detail="Unauthorized role")
#     except Exception as e:
#         raise HTTPException(status_code=401, detail="Invalid or expired token") from e

#     customer = Customer.get_by_id(customer_id)
#     if customer is None:
#         raise HTTPException(status_code=404, detail="Customer not found")

#     try:
#         db.begin_transaction()

#         new_order = Order(user_id=customer_id, amount=0.0, status="processing")
#         new_order.save()

#         item = order_data.item
#         variant = ProductVariant.get_by_id(item.productvariant_id)
#         if variant is None:
#             raise HTTPException(status_code=404, detail="Product variant not found")

#         item_price = variant['price'] if isinstance(variant, dict) else variant.price
#         item_total = item_price * item.product_quantity

#         order_detail = OrderDetail(
#             order_id=new_order.id,
#             variant_id=item.productvariant_id,
#             product_quantity=item.product_quantity,
#             price=item_price
#         )
#         order_detail.save()

#         # Cập nhật tổng tiền
#         update_query = """UPDATE Orders SET amount = %s WHERE id = %s"""
#         db.execute_query(update_query, (item_total, new_order.id))

#         db.commit_transaction()

#         return OrderCheckoutResponse(message="Order created successfully", order_id=new_order.id)

#     except HTTPException:
#         try:
#             db.rollback_transaction()
#         except Exception:
#             pass
#         raise
#     except Exception as e:
#         try:
#             db.rollback_transaction()
#         except Exception:
#             pass
#         raise HTTPException(status_code=500, detail=f"Failed to create order: {e}")


# # Endpoint checkout từ giỏ hàng (mua nhiều sản phẩm)
# @router.post("/checkout", response_model=OrderCheckoutResponse)
# async def checkout(order_data: OrderCheckout):
#     """Tạo đơn hàng từ danh sách sản phẩm (cart_items). Sau khi mua sẽ xóa giỏ hàng."""
#     # Xác thực token và lấy thông tin khách hàng
#     try:
#         payload = verify_access_token(order_data.access_token)
#         customer_id = payload.get("sub")
#         if customer_id is None:
#             raise HTTPException(status_code=401, detail="Invalid token payload")
#         if payload.get("role") != "customer":
#             raise HTTPException(status_code=401, detail="Unauthorized role")
#     except Exception as e:
#         raise HTTPException(status_code=401, detail="Invalid or expired token") from e

#     customer = Customer.get_by_id(customer_id)
#     if customer is None:
#         raise HTTPException(status_code=404, detail="Customer not found")

#     try:
#         db.begin_transaction()

#         new_order = Order(user_id=customer_id, amount=0.0, status="processing")
#         new_order.save()

#         amount = 0.0
#         for item in order_data.cart_items:
#             variant = ProductVariant.get_by_id(item.productvariant_id)
#             if variant is None:
#                 raise HTTPException(status_code=404, detail="Product variant not found")
#             price = variant['price'] if isinstance(variant, dict) else variant.price
#             item_total = price * item.product_quantity
#             amount += item_total

#             order_detail = OrderDetail(
#                 order_id=new_order.id,
#                 variant_id=item.productvariant_id,
#                 product_quantity=item.product_quantity,
#                 price=price
#             )
#             order_detail.save()
#         # Thêm thông tin giao hàng và thanh toán 
#         payment = Payment(
#             payment_method=order_data.payment_method,
#             status="pending",
#             payment_date = None
#         )
#         payment.save()
#         shipment = Shipment(
#             order_id=new_order.id,
#             carrier=order_data.shipment,
#             status= "pending"
#         )
#         shipment.save()
#         # Cập nhật tổng tiền
#         update_query = """UPDATE Orders SET amount = %s WHERE id = %s"""
#         db.execute_query(update_query, (amount, new_order.id))

#         db.commit_transaction()

#         # Clear product bought user's cart after successful purchase
#         try:
#             for item in order_data.cart_items:
#                 Cart.remove_item(customer_id, item.productvariant_id)
#         except Exception:
#             # non-fatal: cart cleanup failed but order succeeded
#             pass

#         return OrderCheckoutResponse(message="Order created successfully", order_id=new_order.id)

#     except HTTPException:
#         try:
#             db.rollback_transaction()
#         except Exception:
#             pass
#         raise
#     except Exception as e:
#         try:
#             db.rollback_transaction()
#         except Exception:
#             pass
#         raise HTTPException(status_code=500, detail=f"Failed to create order: {e}")
# # Các router xem đơn hàng của khách hàng
# @router.get("/my-orders", response_model=List[OrderCheckResponse])
# def get_my_orders(check_data: OrderCheckRequest):
#     # Logic để lấy đơn hàng của khách hàng
#     # Xác thực khách hàng
#     try:
#         payload = verify_access_token(check_data.access_token)
#         customer_id = payload.get("sub")
#         if customer_id is None:
#             raise HTTPException(status_code=401, detail="Invalid token payload")
#         if payload.get("role") != "customer":
#             raise HTTPException(status_code=401, detail="Unauthorized role")
#     except Exception as e:
#         raise HTTPException(status_code=401, detail="Invalid or expired token") from e
#     # Lấy đơn hàng của khách hàng
#     orders = Order.get_user_orders(customer_id)
#     # Lọc theo trạng thái nếu được cung cấp
#     if check_data.status:
#         orders = [order for order in orders if order['status'] == check_data.status]
#     # Trả về danh sách đơn hàng
#     response = []
#     for order in orders:
#         response.append(OrderCheckResponse(
#             order_id=order['id'],
#             user_id=order['user_id'],
#             total_amount=order['total_amount'],
#             status=order['status'],
#             created_at=order['created_at'],
#             updated_at=order['updated_at']
#         ))
#     return response
# # Router để update các đơn hàng (dành cho các đơn hàng đang processing)
# @router.put("/update-status/{order_id}", response_model=OrderStatusUpdateResponse)
# def update_order_status(
#     order_id: int = Path(..., description="ID của đơn hàng cần cập nhật"),
#     status_update: OrderStatusUpdateRequest = ...
# ):
#     # Xác thực token và kiểm tra vai trò nhân viên
#     try:
#         payload = verify_access_token(status_update.access_token)
#         employee_id = payload.get("sub")
#         if employee_id is None:
#             raise HTTPException(status_code=401, detail="Invalid token payload")
#         if payload.get("role") != "employee":
#             raise HTTPException(status_code=401, detail="Unauthorized role")
#     except Exception as e:
#         raise HTTPException(status_code=401, detail="Invalid or expired token") from e

#     employee = Employee.get_by_id(employee_id)
#     if employee is None:
#         raise HTTPException(status_code=404, detail="Employee not found")

#     # Lấy đơn hàng cần cập nhật
#     order = Order.get_by_id(order_id)
#     if order is None:
#         raise HTTPException(status_code=404, detail="Order not found")

#     # Cập nhật trạng thái đơn hàng
#     try:
#         order_model = Order()
#         order_model.update_status(order_id, status_update.new_status)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to update order status: {e}")

#     response = OrderStatusUpdateResponse(
#         order_id=order_id,
#         new_status=status_update.new_status,
#         message="Order status updated successfully"
#     )
#     return response







from fastapi import APIRouter, HTTPException, Query, Path, Header
from typing import List, Optional
from app.schemas import *
from app.models.cart import Cart
from app.models.order import Order
from app.models.order_detail import OrderDetail
from app.models.product_variant import ProductVariant
from app.models.customer import Customer
from app.models.payment import Payment
from app.models.shipment import Shipment
from app.security import verify_access_token
from app.database import db

router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)

# app/routes/orders.py

@router.post("/buy-now", response_model=OrderCheckoutResponse)
async def buy_now(order_data: OrderCheckoutOne):
    """Mua ngay 1 sản phẩm (không xóa giỏ hàng)."""
    
    # 1. Xác thực (Giống hệt checkout)
    try:
        payload = verify_access_token(order_data.access_token)
        customer_id = payload.get("sub")
        if not customer_id: raise HTTPException(status_code=401, detail="Invalid token")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        db.begin_transaction()

        # 2. Tạo Order (Lưu đủ thông tin giao hàng)
        new_order = Order(
            customer_id=customer_id, 
            amount=order_data.total_amount, 
            status="processing",
            
            # Lấy thông tin từ frontend gửi lên
            shipping_name=order_data.customer_info.name,
            shipping_phone=order_data.customer_info.phone,
            shipping_address=order_data.customer_info.address
        )
        new_order_id = new_order.save()

        # 3. Tạo Order Detail (Xử lý 1 món duy nhất từ biến 'item')
        item = order_data.item
        variant = ProductVariant.get_by_id(item.productvariant_id)
        if not variant:
            raise HTTPException(status_code=404, detail="Product variant not found")

        real_price = float(variant['price'])
        
        order_detail = OrderDetail(
            order_id=new_order_id,
            variant_id=item.productvariant_id,
            product_quantity=item.product_quantity,
            price=real_price
        )
        order_detail.save()

        # 4. Tạo Payment (Dùng Shared ID)
        payment = Payment(
            order_id=new_order_id,
            payment_method=order_data.payment_method,
            status="pending"
        )
        payment.save()

        # 5. Tạo Shipment
        shipment = Shipment(
            order_id=new_order_id, 
            carrier=order_data.shipment,
            status="pending"
        )
        shipment.save()

        # 6. KHÔNG XÓA GIỎ HÀNG (Sự khác biệt duy nhất với Checkout)

        db.commit_transaction()

        return OrderCheckoutResponse(message="Buy Now order created", order_id=new_order_id)

    except Exception as e:
        db.rollback_transaction()
        print(f"BUY NOW ERROR: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# --- ENDPOINT CHECKOUT (Mua từ giỏ hàng) ---
@router.post("/checkout", response_model=OrderCheckoutResponse)
async def checkout(order_data: OrderCheckout):
    try:
        payload = verify_access_token(order_data.access_token)
        customer_id = payload.get("sub")
        if not customer_id: raise HTTPException(status_code=401, detail="Invalid token")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    # 1. Bắt đầu giao dịch
    try:
        db.begin_transaction()

        # 2. Tạo đơn hàng (Lưu thông tin người nhận)
        new_order = Order(
            customer_id=customer_id, 
            amount=order_data.total_amount, # Lấy luôn tổng tiền từ Frontend gửi lên (hoặc tính lại)
            status="processing",

            shipping_name=order_data.customer_info.name,
            shipping_phone=order_data.customer_info.phone,
            shipping_address=order_data.customer_info.address
        )
        new_order_id = new_order.save() # Giả sử hàm save trả về ID

        # 3. Lưu chi tiết đơn hàng (Order Details)
        for item in order_data.cart_items:
            # Lấy giá từ DB để bảo mật (không tin tưởng giá từ frontend)
            variant = ProductVariant.get_by_id(item.productvariant_id)
            if not variant:
                raise HTTPException(status_code=404, detail=f"Variant {item.productvariant_id} not found")
            
            real_price = float(variant['price'])
            
            order_detail = OrderDetail(
                order_id=new_order_id,
                variant_id=item.productvariant_id,
                product_quantity=item.product_quantity,
                price=real_price
            )
            order_detail.save()

        # 4. Tạo Thanh toán (Payment)
        payment = Payment(
            order_id=new_order_id, 
            payment_method=order_data.payment_method,
            status="pending"
        )
        payment.save()

        # 5. Tạo Vận chuyển (Shipment)
        shipment = Shipment(
            order_id=new_order_id, 
            carrier=order_data.shipment,
            status="pending"
        )
        shipment.save()

        # 6. Cam kết giao dịch
        db.commit_transaction()

        # 7. Xóa giỏ hàng (Sau khi thành công)
        try:
            # Xóa các món đã mua khỏi giỏ (dựa vào danh sách items gửi lên)
            for item in order_data.cart_items:
                Cart.remove_item(customer_id, item.productvariant_id)
        except Exception:
            pass # Lỗi xóa giỏ hàng không ảnh hưởng đơn hàng

        return OrderCheckoutResponse(message="Order created successfully", order_id=new_order_id)

    except Exception as e:
        db.rollback_transaction()
        print(f"ORDER ERROR: {e}") # Log lỗi để debug
        raise HTTPException(status_code=500, detail=str(e))


# --- ENDPOINT XEM ĐƠN HÀNG (Sửa lại thành GET chuẩn) ---
@router.get("/my-orders", response_model=List[OrderCheckResponse])
def get_my_orders(
    access_token: str = Query(...), 
    status: Optional[str] = Query(None)
):
    try:
        payload = verify_access_token(access_token)
        customer_id = payload.get("sub")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    orders = Order.get_user_orders(customer_id)
    
    if status:
        orders = [o for o in orders if o['status'] == status]

    # Convert dữ liệu DB sang Schema Response
    response = []
    for order in orders:
        response.append(OrderCheckResponse(
            order_id=order['id'],
            # ... map các trường khác ...
            status=order['status'],
            total_amount=order['amount']
        ))
    return response