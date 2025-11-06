from passlib.context import CryptContext

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