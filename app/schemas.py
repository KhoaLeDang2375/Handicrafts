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
class Token(BaseModel):
    access_token: str
    token_type: str
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
    date: Optional[str] = None
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
# Pydantic schemas for Order Checkout
class OrderCheckout(BaseModel):
    access_token: str
    cart_items: List[CartItemBase]
    payment_method: str = "COD"
    shipment : str = "GHTK"
class OrderCheckoutOne(BaseModel):
    access_token: str
    item: CartItemBase
    payment_method: str = "COD"
    shipment : str = "GHTK"
class OrderStatusUpdateRequest(BaseModel):
    access_token: str
    new_status: str = 'Waiting for delivery'
class OrderStatusUpdateResponse(BaseModel):
    order_id: int
    new_status: str
    message: str = "Order status updated successfully"
# Chúng ta lấy user_id từ access token
class OrderCheckoutResponse(BaseModel):
    message: str
    order_id: int
# Pydantic schemas for Order Check
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
    access_token: str
    status: str = None
class OrderCheckResponse(BaseModel):
    order_id: int
    items: list[OrderDetailResponse]
    price: float
    status: str = None
