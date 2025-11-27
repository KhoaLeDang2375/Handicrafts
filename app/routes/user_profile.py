from fastapi import APIRouter, HTTPException, Query, Path,Depends, status, Header
from typing import List, Optional
from app.schemas import *
import json
from app.models.employee import Employee
from app.models.customer import Customer
from app.models.media import Media
from app.security import verify_access_token
router = APIRouter(
    prefix="/my-profile",
    tags=["my-profile"]
)
def get_current_user_payload(authorization: str = Header(..., alias="Authorization")):
    """
    Dependency dùng để lấy và xác thực token từ Header.
    Format bắt buộc: 'Bearer <token_string>'
    """
    
    # Định nghĩa lỗi chung để tái sử dụng
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # 1. Tách chuỗi "Bearer" và "Token"
        # authorization.split() sẽ tách chuỗi dựa trên khoảng trắng
        scheme, token = authorization.split()
        
        # 2. Kiểm tra xem có đúng là "Bearer" không
        if scheme.lower() != 'bearer':
            raise credentials_exception
            
        # 3. Gọi hàm giải mã token của bạn
        # Lưu ý: Hàm verify_access_token cần raise Exception nếu hết hạn hoặc sai key
        payload = verify_access_token(token)
        
        # 4. Kiểm tra các thông tin quan trọng trong payload
        user_id = payload.get("sub")
        role = payload.get("role")
        
        if user_id is None or role is None:
            raise credentials_exception
            
        # 5. Trả về payload sạch để dùng trong Endpoint
        return {"user_id": user_id, "role": role}

    except ValueError:
        # Lỗi này xảy ra nếu header không có khoảng trắng (VD: gửi mỗi token mà không có chữ Bearer)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication header format. Expected 'Bearer <token>'",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        # Bắt các lỗi từ verify_access_token (như TokenExpired, JWTError)
        # Bạn có thể in e ra để debug: print(f"Token Error: {e}")
        raise credentials_exception
@router.get("/",response_model=UserProfileResponse)
async def get_my_profile(payload: dict = Depends(get_current_user_payload)):
    try:
        user_id = payload.get("user_id")
        role = payload.get('role')
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        if payload.get("role") is None:
            raise HTTPException(status_code=401, detail="Unauthorized role")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    avt_url = Media.get_by_entity(user_id,"customer")
    user_profile = None
    user_profile = None

    if role == 'customer':
        user_profile = Customer.get_by_id(user_id)
    elif role == 'employee':
        user_profile = Employee.get_by_id(user_id)
    if user_profile is None:
        # Nếu không tìm thấy profile, trả về lỗi 404
        raise HTTPException(status_code=404, detail="User profile not found in database for the given role.")
    return UserProfileResponse(
        email= user_profile['email'],
        address= user_profile['address'],
        full_name = user_profile['name'],
        avatar_url = avt_url.url if avt_url else None,
        phone_number = user_profile['phone']
    ) 

@router.put("/", response_model=UserProfileUpdateResponse)
async def update_my_profile(
    update_req: UserUpdateProfileRequest,
    payload: dict = Depends(get_current_user_payload) 
):
    user_id = payload["user_id"]
    role = payload["role"]

    # 1. Chuyển đổi request model thành dictionary, loại bỏ các giá trị None
    # exclude_unset=True nghĩa là trường nào user không gửi thì không update
    update_data = update_req.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="No data provided for update")

    # 2. Thực hiện Update vào DB
    is_updated = False
    
    if role == 'customer':
        # Tạo dummy object để gọi hàm update (hoặc chuyển hàm update thành @staticmethod)
        customer_obj = Customer(None, None, None, None, None, None) 
        is_updated = customer_obj.update(user_id, update_data)
        
    elif role == 'employee':
        # Tương tự cho Employee
        employee_obj = Employee(None, None, None, None, None, None)
        is_updated = employee_obj.update(user_id, update_data)

    if not is_updated:
        raise HTTPException(status_code=500, detail="Failed to update profile or no changes made")

    return UserProfileUpdateResponse(
        msg="Update Success!",
        updated_fields=list(update_data.keys())
    )