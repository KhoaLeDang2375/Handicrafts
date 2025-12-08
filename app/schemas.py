from pydantic import BaseModel, Field, EmailStr, ValidationError
from typing import List, Optional
from enum import Enum
import re
from datetime import datetime
from pydantic import BaseModel, Field, constr, confloat, conint
from typing import Optional
# Pydantic models product
class ProductVariantBase(BaseModel):
    color: str
    size: Optional[int] = None
    price: float
    amount: int

class ProductVariantResponse(ProductVariantBase):
    id: int
    product_id: int

class CategoryBase(BaseModel):
    id: int
    name: str

class ProductCreate(BaseModel):
    access_token: str
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
class UpdateBase(BaseModel):
    """
    Schema tổng quát cho các yêu cầu cập nhật (update) có xác thực.
    Dùng cho cả Product, ProductVariant, v.v.
    """
    access_token: str = Field(
        ..., 
        description="JWT access token để xác thực người thực hiện hành động"
    )
    #  Các trường chung có thể xuất hiện trong bất kỳ loại cập nhật nào

    name: Optional[str] = Field(
        None, description="Tên sản phẩm hoặc biến thể"
    )
    description: Optional[str] = Field(
        None, description="Mô tả sản phẩm"
    )
    artisan_description: Optional[str] = Field(
        None, description="Thông tin nghệ nhân hoặc mô tả thủ công"
    )
    status: Optional[int] = Field(
        None, ge=0, le=1, description="Trạng thái: 1 = hoạt động, 0 = ẩn"
    )
    category_id: Optional[int] = Field(None, description="Mã danh mục sản phẩm")
    color: Optional[str] = Field(None, description="Màu biến thể")
    size: Optional[str] = Field(None, description="Kích thước biến thể")
    price: Optional[float] = Field(None, description="Giá bán")
    amount: Optional[int] = Field(None, description="Số lượng tồn kho")
# Product variant update response schemas
class ProductVariantUpdateResponse(BaseModel):
    id:int
    product_id: int
    message: str = 'Product variant updated successfully'
PHONE_REGEX = r'^0[0-9]{9}$'
# Pydantic schemas user sign up
class EmployeeCreate(BaseModel):
    name: str 
    email: EmailStr
    job_title: str
    username: str
    password: str
    phone_number: str = Field(
        ..., # Bắt buộc phải có
        pattern=PHONE_REGEX,
        description="Số điện thoại phải là 10 chữ số, bắt đầu bằng 0."
    )
class EmployeeCreateResponse(BaseModel):
    message: str
    email: EmailStr
    fullname: str   
class CustomerCreate(BaseModel):
    name: str 
    email: EmailStr
    address: str
    username: str
    password: str
    phone_number: str = Field(
        ..., # Bắt buộc phải có
        pattern=PHONE_REGEX,
        description="Số điện thoại phải là 10 chữ số, bắt đầu bằng 0."
    )
class CustomerCreateResponse(BaseModel):
    message: str
    email: EmailStr
    fullname: str

class RoleEnum(str, Enum):
    customer = 'customer'
    employee = 'employee'

# Pydantic schemas user login 
class LoginRequest(BaseModel):
    username: Optional[str] = None
    password: str
    role: RoleEnum = Field(..., description="Customer hoặc Employee")

class UserInfo(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str
    user_info: Optional[UserInfo] = None
# Pydantic schemas review
class ReviewCreate(BaseModel):
    access_token: str
    rating: int = Field(..., ge=1, le=5)
    content: Optional[str] = None


class ReviewResponse(BaseModel):
    id: int
    customer_id: int
    variant_id: int
    rating: int
    content: Optional[str] = None
    date: Optional[datetime] = None
    customer_name: Optional[str] = None
    product_name: Optional[str] = None

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat() if dt else None
        }

class ReviewUpdate(BaseModel):
    access_token: str
    rating: Optional[int] = Field(None, ge=1, le=5)
    content: Optional[str] = None

class ReviewDelete(BaseModel):
    access_token: str
# Pydantic schemas blog
class BlogBase(BaseModel):
    title: str
    content: str
class BlogResponse(BlogBase):
    id: int
    author_id: int
    create_time: Optional[datetime] = None
    model_config = {
        "json_encoders": {datetime: str},
        "arbitrary_types_allowed": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "author_id": 1,
                "title": "Sample Blog",
                "content": "Sample content",
                "create_time": "2024-10-15T10:15:00"
            }
        }
    }
    
class PaginatedReviewList(BaseModel):
    items: List[ReviewResponse]
    total: int
    skip: int
    limit: int
# Pydantic schemas for Cart
class CartItemBase(BaseModel):
    product_id: int
    productvariant_id: int
    product_quantity: int
class CartItemResponse(CartItemBase):
    id: int
    user_id: int
    total_price: float
    color: Optional[str] = None
    size: Optional[int] = None
    price: Optional[float] = None
    product_name: Optional[str] = None
    stock_quantity: int
# Pydantic schemas for Order Checkout
# class OrderCheckout(BaseModel):
#     access_token: str
#     cart_items: List[CartItemBase]
#     payment_method: str = "COD"
#     shipment : str = "GHTK"
#     total_amount: float # Tổng tiền đơn hàng 
# class OrderCheckoutOne(BaseModel):
#     access_token: str
#     item: CartItemBase
#     payment_method: str = "COD" 
#     shipment : str = "GHTK"
# class OrderStatusUpdateRequest(BaseModel):
#     access_token: str
#     new_status: str = 'Waiting for delivery'
# class OrderStatusUpdateResponse(BaseModel):
#     order_id: int
#     new_status: str
#     message: str = "Order status updated successfully"
# # Chúng ta lấy user_id từ access token
# class OrderCheckoutResponse(BaseModel):
#     message: str
#     order_id: int
# # Pydantic schemas for Order Check
# class OrderDetailResponse(BaseModel):
#     id: int
#     order_id: int
#     productvariant_id: int
#     product_name: Optional[str] = None
#     color: Optional[str] = None
#     size: Optional[int] = None
#     quantity: int
#     price: float
# class OrderCheckRequest(BaseModel):
#     access_token: str
#     status: str = None
# class OrderCheckResponse(BaseModel):
#     order_id: int
#     items: list[OrderDetailResponse]
#     price: float
#     status: str = None
# Pydantic schemas for Cart Response
class CartResponse(BaseModel):
    customer_id: int
    items: List[CartItemResponse] = []
    total_amount: float = 0.0
# Pydantic schemas for adding item to Cart
class CartItemAdd(BaseModel):
    access_token: str
    productvariant_id: int
    product_quantity: int
class CartItemAddResponse(BaseModel):
    productvariant_id: int
    quantity: int
    total_price: float
    message: str = "Item added to cart successfully"
# Pydantic schemas for updating item in Cart
class CartItemUpdate(BaseModel):
    access_token: str
    productvariant_id: int
    new_quantity: int
class CartItemUpdateResponse(BaseModel):
    productvariant_id: int
    quantity: int
    total_price: float
    message: str = "Cart item updated successfully"
# Pydantic schemas for removing item from Cart
class CartItemDeleteResponse(BaseModel):
    productvariant_id: int
    message: str = "Item removed from cart successfully"
# User profile schemas
# Model base chứa các trường chung
class UserRequest(BaseModel):
    access_token: str

class OrderHistoryItem(BaseModel):
    order_id: int     
    status: str
    date: datetime
    total_products: int
    total_amount: float
class UserProfileResponse(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    address :  Optional[str] = None
    avatar_url: Optional[str] = None
    phone_number: Optional[str] = None
    orders: List[OrderHistoryItem] = []
    # Cấu hình này giúp Pydantic đọc dữ liệu từ ORM (SQLAlchemy/SQLModel)
    class Config:
        from_attributes = True
class UserUpdateProfileRequest(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=50)
    address: Optional[str] = Field(None, max_length=200)
    phone_number: Optional[str] = Field(None, pattern=r"(84|0[3|5|7|8|9])+([0-9]{8})\b") # Regex số ĐT VN
    email: Optional[EmailStr] = None # Thường ít khi cho đổi email tùy tiện, nhưng cứ để đây nếu bạn cần
# Response: Trả về thông báo và dữ liệu sau khi update
class UserProfileUpdateResponse(BaseModel):
    msg: str = "Updated Successfully!"
    updated_fields: list[str] # Danh sách các trường đã được update'










# ==========================================
# ORDER (THANH TOÁN) 
# ==========================================

# --- Schema phụ để nhận thông tin từ form Frontend ---
class CustomerInfoRequest(BaseModel):
    name: str
    phone: str
    email: str
    address: str
    note: Optional[str] = None

# --- Schema phụ để nhận từng món hàng khi đặt hàng ---
class OrderItemRequest(BaseModel):
    productvariant_id: int
    product_quantity: int

# --- Schema cho Checkout từ Giỏ hàng ---
class OrderCheckout(BaseModel):
    access_token: str
    cart_items: List[OrderItemRequest] # Danh sách món hàng
    customer_info: CustomerInfoRequest # Thông tin người nhận
    
    payment_method: str = "COD"
    shipment: str = "GHTK"
    total_amount: float # Tổng tiền đơn hàng

# --- Schema cho Mua Ngay (1 món) ---
class OrderCheckoutOne(BaseModel):
    access_token: str
    item: OrderItemRequest # Chỉ 1 món hàng
    customer_info: CustomerInfoRequest # Thông tin người nhận
    
    payment_method: str = "COD"
    shipment: str = "GHTK"
    total_amount: float

# --- Response sau khi đặt hàng ---
class OrderCheckoutResponse(BaseModel):
    message: str
    order_id: int

# --- Schema Update trạng thái đơn hàng (Employee) ---
class OrderStatusUpdateRequest(BaseModel):
    access_token: str
    new_status: str = 'Waiting for delivery'

class OrderStatusUpdateResponse(BaseModel):
    order_id: int
    new_status: str
    message: str = "Order status updated successfully"

# --- Schema Xem đơn hàng (History) ---
class OrderDetailResponse(BaseModel):
    id: int
    order_id: int
    productvariant_id: int
    product_name: Optional[str] = None
    color: Optional[str] = None
    size: Optional[int] = None
    quantity: int
    price: float

class OrderCheckRequest(BaseModel):
    # Dùng khi client gửi request body (Lưu ý: GET request nên dùng Query param thay vì body)
    access_token: str
    status: Optional[str] = None

class OrderCheckResponse(BaseModel):
    order_id: int
    items: List[OrderDetailResponse]
    total_amount: float 
    status: Optional[str] = None
    created_at: Optional[datetime] = None
    total_products: int


# ==========================================
# CONTACTFORM (Liên hệ)
# ==========================================
class ContactCreateRequest(BaseModel):
    content: str

# Response: Dữ liệu trả về 
class ContactResponse(BaseModel):
    id: int
    content: str
    create_time: datetime
    sender_name: Optional[str] = None