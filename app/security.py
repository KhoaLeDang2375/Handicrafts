from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWSError, jwt
from dotenv import load_dotenv
import os
load_dotenv()
# Khởi tạo CryptContext với thuật toán bcrypt.
# bcrypt là một hàm băm chậm (costly) được thiết kế đặc biệt cho mật khẩu.
# 'deprecated="auto"' nghĩa là passlib sẽ tự động nâng cấp nếu cần.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hàm băm (hash) mật khẩu.
    Chỉ dùng khi Đăng ký (Register)
    """
    truncated_password = password[:72]
    # để tạo ra một chuỗi băm (hash) an toàn.
    return pwd_context.hash(truncated_password)
SECRET_KEY = os.getenv('SERCET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token hết hạn sau 30 phút
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Tạo ra một Access Token (JWT)
    data: Dữ liệu bạn muốn lưu vào Payload (ví dụ: email/username)
    """
    to_encode = data.copy()
    # Tinh thoi gina het han
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Hàm xác minh mật khẩu.
    Dùng khi Đăng nhập (Login)
    
    Tham số:
    - plain_password: Mật khẩu dạng văn bản gốc mà người dùng nhập vào.
    - hashed_password: Chuỗi mật khẩu đã băm được lưu trong Cơ sở dữ liệu.
    
    Trả về: True nếu khớp, False nếu không khớp.
    """
    # pwd_context.verify() sẽ tự động lấy salt từ hashed_password, 
    # băm plain_password và so sánh hai chuỗi băm.
    return pwd_context.verify(plain_password, hashed_password)