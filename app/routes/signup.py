from fastapi import APIRouter, HTTPException
from app.schemas import CustomerCreate, CustomerCreateResponse
from app.models.customer import Customer
from app.security import hash_password

router = APIRouter(
    prefix="/register",
    tags=["customersignup"]
)

@router.post("/signup", response_model=CustomerCreateResponse)
async def signup(customer: CustomerCreate):
    """Thực hiện chức năng đăng ký cho người dùng"""
    # Kiểm tra email đã tồn tại chưa
    existing_user = Customer.get_by_email(customer.email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email đã được sử dụng"
        )

    try:
        # Hash mật khẩu trước khi lưu
        customer_password_hashed = hash_password(customer.password)
        
        # Tạo customer mới
        new_customer = Customer(
            name=customer.name,
            address=customer.address,
            email=customer.email,
            phone=customer.phone_number,
            username=customer.username,
            password=customer_password_hashed
        )
        
        # Lưu vào database
        new_customer.save()
        
        return CustomerCreateResponse(
            message="Đăng ký thành công",
            email=customer.email,
            fullname=customer.name
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Có lỗi xảy ra khi đăng ký: {str(e)}"
        )
