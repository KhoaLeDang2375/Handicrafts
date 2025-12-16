from werkzeug.security import generate_password_hash

# Tạo hash cho mật khẩu "1234"
hash_string = generate_password_hash("1234")
print(hash_string)