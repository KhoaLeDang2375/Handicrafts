# from fastapi import APIRouter, HTTPException, Query, Path,Depends, status, Header
# from typing import List, Optional
# from app.schemas import *
# import json
# from app.models.employee import Employee
# from app.models.customer import Customer
# from app.models.media import Media
# from app.security import verify_access_token
# router = APIRouter(
#     prefix="/my-profile",
#     tags=["my-profile"]
# )
# def get_current_user_payload(authorization: str = Header(..., alias="Authorization")):
#     """
#     Dependency dùng để lấy và xác thực token từ Header.
#     Format bắt buộc: 'Bearer <token_string>'
#     """
    
#     # Định nghĩa lỗi chung để tái sử dụng
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )

#     try:
#         # 1. Tách chuỗi "Bearer" và "Token"
#         # authorization.split() sẽ tách chuỗi dựa trên khoảng trắng
#         scheme, token = authorization.split()
        
#         # 2. Kiểm tra xem có đúng là "Bearer" không
#         if scheme.lower() != 'bearer':
#             raise credentials_exception
            
#         # 3. Gọi hàm giải mã token của bạn
#         # Lưu ý: Hàm verify_access_token cần raise Exception nếu hết hạn hoặc sai key
#         payload = verify_access_token(token)
        
#         # 4. Kiểm tra các thông tin quan trọng trong payload
#         user_id = payload.get("sub")
#         role = payload.get("role")
        
#         if user_id is None or role is None:
#             raise credentials_exception
            
#         # 5. Trả về payload sạch để dùng trong Endpoint
#         return {"user_id": user_id, "role": role}

#     except ValueError:
#         # Lỗi này xảy ra nếu header không có khoảng trắng (VD: gửi mỗi token mà không có chữ Bearer)
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication header format. Expected 'Bearer <token>'",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     except Exception as e:
#         # Bắt các lỗi từ verify_access_token (như TokenExpired, JWTError)
#         # Bạn có thể in e ra để debug: print(f"Token Error: {e}")
#         raise credentials_exception
# @router.get("/",response_model=UserProfileResponse)
# async def get_my_profile(payload: dict = Depends(get_current_user_payload)):
#     try:
#         user_id = payload.get("user_id")
#         role = payload.get('role')
#         if user_id is None:
#             raise HTTPException(status_code=401, detail="Invalid token payload")
#         if payload.get("role") is None:
#             raise HTTPException(status_code=401, detail="Unauthorized role")
#     except Exception as e:
#         raise HTTPException(status_code=401, detail="Invalid or expired token")
#     avt_url = Media.get_by_entity(user_id,"customer")
#     user_profile = None
#     user_profile = None

#     if role == 'customer':
#         user_profile = Customer.get_by_id(user_id)
#     elif role == 'employee':
#         user_profile = Employee.get_by_id(user_id)
#     if user_profile is None:
#         # Nếu không tìm thấy profile, trả về lỗi 404
#         raise HTTPException(status_code=404, detail="User profile not found in database for the given role.")
#     return UserProfileResponse(
#         email= user_profile['email'],
#         address= user_profile['address'],
#         full_name = user_profile['name'],
#         avatar_url = avt_url.url if avt_url else None,
#         phone_number = user_profile['phone']
#     ) 

# @router.put("/", response_model=UserProfileUpdateResponse)
# async def update_my_profile(
#     update_req: UserUpdateProfileRequest,
#     payload: dict = Depends(get_current_user_payload) 
# ):
#     user_id = payload["user_id"]
#     role = payload["role"]

#     # 1. Chuyển đổi request model thành dictionary, loại bỏ các giá trị None
#     # exclude_unset=True nghĩa là trường nào user không gửi thì không update
#     update_data = update_req.model_dump(exclude_unset=True)

#     if not update_data:
#         raise HTTPException(status_code=400, detail="No data provided for update")

#     # 2. Thực hiện Update vào DB
#     is_updated = False
    
#     if role == 'customer':
#         # Tạo dummy object để gọi hàm update (hoặc chuyển hàm update thành @staticmethod)
#         customer_obj = Customer(None, None, None, None, None, None) 
#         is_updated = customer_obj.update(user_id, update_data)
        
#     elif role == 'employee':
#         # Tương tự cho Employee
#         employee_obj = Employee(None, None, None, None, None, None)
#         is_updated = employee_obj.update(user_id, update_data)

#     if not is_updated:
#         raise HTTPException(status_code=500, detail="Failed to update profile or no changes made")

#     return UserProfileUpdateResponse(
#         msg="Update Success!",
#         updated_fields=list(update_data.keys())
#     )


from fastapi import APIRouter, HTTPException, Query, Path, Depends, status, Header
from typing import List, Optional
from app.models.employee import Employee
from app.models.customer import Customer
from app.models.media import Media
from app.models.order import Order 
from app.schemas import UserProfileResponse, UserUpdateProfileRequest, UserProfileUpdateResponse
from app.security import verify_access_token

router = APIRouter(
    prefix="/my-profile",
    tags=["my-profile"]
)

# --- DEPENDENCY (Nên tách ra file dependencies.py) ---
def get_current_user_payload(authorization: str = Header(..., alias="Authorization")):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        scheme, token = authorization.split()
        if scheme.lower() != 'bearer':
            raise credentials_exception
        
        payload = verify_access_token(token)
        user_id = payload.get("sub")
        role = payload.get("role")
        
        if user_id is None or role is None:
            raise credentials_exception
            
        return {"user_id": user_id, "role": role}

    except (ValueError, Exception):
        raise credentials_exception

# --- GET PROFILE (bổ sung Order History) ---
@router.get("/", response_model=UserProfileResponse)
async def get_my_profile(payload: dict = Depends(get_current_user_payload)):
    user_id = payload["user_id"]
    role = payload["role"]
    
    user_profile = None
    orders_history = [] # List chứa lịch sử đơn hàng

    # 1. Lấy thông tin User và Order History dựa theo Role
    if role == 'customer':
        user_profile = Customer.get_by_id(user_id)
        # Gọi hàm lấy đơn hàng kèm số lượng sản phẩm
        orders_history = Order.get_orders_by_customer(user_id) 
        
    elif role == 'employee':
        user_profile = Employee.get_by_id(user_id)
        # Employee không có lịch sử mua hàng cá nhân
        orders_history = [] 

    if user_profile is None:
        raise HTTPException(status_code=404, detail="User profile not found.")

    # 2. Lấy Avatar (Dùng role động thay vì fix cứng "customer")
    # Lưu ý: role trong token thường là 'customer'/'employee', check lại DB xem cột entity_type lưu là gì
    avt_obj = Media.get_by_entity(user_id, role) 
    avt_url = avt_obj.url if avt_obj else None

    # 3. Trả về đúng Schema (Schema update thêm trường orders)
    return UserProfileResponse(
        email=user_profile['email'],
        address=user_profile['address'],
        full_name=user_profile['name'], 
        phone_number=user_profile['phone'],
        avatar_url=avt_url,
        orders=orders_history
    ) 

# --- UPDATE PROFILE ---
@router.put("/", response_model=UserProfileUpdateResponse)
async def update_my_profile(
    update_req: UserUpdateProfileRequest,
    payload: dict = Depends(get_current_user_payload) 
):
    user_id = payload["user_id"]
    role = payload["role"]

    update_data = update_req.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No data provided for update")

    is_updated = False
    
    # Trong class Customer/Employee, hàm update nên có @staticmethod
    if role == 'customer':
        is_updated = Customer.update(user_id, update_data)
    elif role == 'employee':
        is_updated = Employee.update(user_id, update_data)

    if not is_updated:
        # Có thể return success=False thay vì 500 nếu đó không phải lỗi hệ thống
        raise HTTPException(status_code=500, detail="Failed to update. User might not exist.")

    return UserProfileUpdateResponse(
        msg="Update Success!",
        updated_fields=list(update_data.keys())
    )