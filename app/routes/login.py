from fastapi import APIRouter, HTTPException,status
from app.schemas import LoginRequest, Token
from app.models.customer import Customer
from app.models.employee import Employee
from app.security import *
from werkzeug.security import check_password_hash
router = APIRouter(
    prefix="/login",
    tags=["login"]
)
@router.post("/", response_model=Token)
async def login_for_access_token(login_request: LoginRequest):
    """
    Xác thực người dùng (Customer hoặc Employee) và trả về JWT.
    """
    user = None
    hashed_password = None
    password_ok = False

    if login_request.role == 'customer':
        user = Customer.get_by_username(login_request.username)
        if user:
            hashed_password = user.get('password')
            # customers use passlib bcrypt via app.security.hash_password
            password_ok = verify_password(login_request.password, hashed_password) if hashed_password else False
    elif login_request.role == 'employee':
        user = Employee.get_by_username(login_request.username)
        # Thêm kiểm tra status
        if user.get('status') != 'active':
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Tài khoản nhân viên chưa được kích hoạt."
            )
        if user:
            hashed_password = user.get('password')
            # employees were hashed using werkzeug.generate_password_hash in Employee.save
            password_ok = check_password_hash(hashed_password, login_request.password) if hashed_password else False
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vai trò không hợp lệ."
        )

    if not user or not hashed_password or not password_ok:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tên đăng nhập hoặc mật khẩu không chính xác",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data = {
            "sub": str(user.get('id')),   # Convert id to string
            "role": login_request.role,
            "name": user.get('name')  # nếu cần
}
    )
    return {"access_token": access_token, "token_type": "bearer"}