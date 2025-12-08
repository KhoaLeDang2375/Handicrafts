from fastapi import APIRouter, HTTPException, Depends, Header
from app.schemas import ContactCreateRequest
from app.models.contact_form import ContactForm # Import class bạn đã cung cấp
from app.security import verify_access_token

router = APIRouter(
    prefix="/contact",
    tags=["contact"]
)

# Hàm phụ trợ để lấy user từ token (tái sử dụng từ các route khác)
def get_current_user_optional(authorization: str = Header(None)):
    """
    Hàm này trả về user_id nếu có token hợp lệ, ngược lại trả về None.
    Dùng cho trường hợp khách vãng lai (Guest) cũng có thể gửi liên hệ.
    """
    if not authorization:
        return None
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != 'bearer':
            return None
        payload = verify_access_token(token)
        return payload.get("sub") # Trả về customer_id
    except:
        return None

@router.post("/")
async def create_contact(
    request: ContactCreateRequest,
    user_id: str = Depends(get_current_user_optional)
):
    try:
        # 1. Khởi tạo đối tượng ContactForm
        # Nếu user_id có (đã login) -> customer_id = user_id
        # Nếu không (khách vãng lai) -> customer_id = None
        new_contact = ContactForm(
            content=request.content,
            contact_type="customer",
            customer_id=user_id, 
            employee_id=None
        )

        # 2. Lưu vào Database
        result = new_contact.save()
        
        if result:
            return {"message": "Gửi liên hệ thành công!", "success": True}
        else:
            raise HTTPException(status_code=500, detail="Lỗi khi lưu vào database")

    except Exception as e:
        print(f"Error creating contact: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")