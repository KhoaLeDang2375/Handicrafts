from pydantic import BaseModel, Field, EmailStr, ValidationError
from typing import List, Optional
from enum import Enum
import re
from datetime import datetime

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
    status: str = None
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


class SearchResult(BaseModel):
    product_id: int
    name: str
    description: Optional[str] = None
    category_name: Optional[str] = None
    score: float

class SearchResults(BaseModel):
    items: List[SearchResult]
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
    customer_id: int
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
    rating: Optional[int] = Field(None, ge=1, le=5)
    content: Optional[str] = None

class PaginatedReviewList(BaseModel):
    items: List[ReviewResponse]
    total: int
    skip: int
    limit: int