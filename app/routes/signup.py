from fastapi import APIRouter, HTTPException
from app.models.employee import Employee
from app.schemas import CustomerCreate, CustomerCreateResponse, EmployeeCreateResponse, EmployeeCreate
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
@router.post("/employee-signup", response_model=EmployeeCreateResponse)
async def employee_signup(employee: EmployeeCreate):
    """Thực hiện chức năng đăng ký cho nhân viên"""
    # Kiểm tra email đã tồn tại chưa
    existing_user = Employee.get_by_email(employee.email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email đã được sử dụng"
        )
    try:
        # Hash mật khẩu trước khi lưu
        employee_password_hashed = hash_password(employee.password)
        # Kiểm tra job title hợp lệ
        if employee.job_title not in ['Quản lý', 'Nhân viên kinh doanh', 'Nhân viên kho', 'Nhân viên marketing']:
            raise HTTPException(
                status_code=400,
                detail="Job title không hợp lệ"
            )
        # Tạo employee mới
        new_employee = Employee(
            name=employee.name,
            job_title=employee.job_title,
            email=employee.email,
            phone=employee.phone_number,
            user_name=employee.username,
            password=employee_password_hashed
        )
        
        # Lưu vào database
        new_employee.save()
        
        return EmployeeCreateResponse(
            message="Yêu cầu đang chờ duyệt",
            email=employee.email,
            fullname=employee.name
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Có lỗi xảy ra khi đăng ký nhân viên: {str(e)}"
        )
