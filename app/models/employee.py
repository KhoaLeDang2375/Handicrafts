from app.database import db
from werkzeug.security import generate_password_hash, check_password_hash

class Employee:
    def __init__(self, name, phone, job_title, user_name, password,email):
        self.name = name
        self.phone = phone
        self.job_title = job_title
        self.user_name = user_name
        self.password = generate_password_hash(password)
        self.email = email

    def save(self):
        query = """
        INSERT INTO Employee (name, phone, job_title, user_name, password,email)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        return db.execute_query(query, (
            self.name,
            self.phone,
            self.job_title,
            self.user_name,
            self.password,
            self.email
        ))

    @staticmethod
    def get_by_id(employee_id):
        query = """SELECT * FROM Employee WHERE id = %s"""
        return db.fetch_one(query, (employee_id,))

    @staticmethod
    def get_by_username(username):
        query = """SELECT * FROM Employee WHERE user_name = %s"""
        return db.fetch_one(query, (username,))
    @staticmethod
    def get_by_email(email):
        query = """SELECT * FROM Employee WHERE email = %s"""
        return db.fetch_one(query, (email,))

    @staticmethod
    def get_all():
        query = """SELECT id, name, phone, job_title, user_name, email FROM Employee"""
        return db.fetch_all(query)

# Trong file chứa class Customer
    def update(self, user_id, update_data: dict):
        """
        Hàm update động.
        update_data: Dictionary chứa các trường cần sửa. VD: {'name': 'Mới', 'address': 'HN'}
        """
        if not update_data:
            return False

        # Mapping tên trường từ Pydantic (snake_case) sang tên cột trong DB
        # Key: Pydantic field, Value: DB Column name
        field_mapping = {
            "full_name": "name",
            "address": "address",
            "phone_number": "phone",
            "email": "email"
        }

        set_clauses = []
        values = []

        # Xây dựng câu SQL động
        for key, value in update_data.items():
            if key in field_mapping and value is not None:
                col_name = field_mapping[key]
                set_clauses.append(f"{col_name} = %s")
                values.append(value)
        
        if not set_clauses:
            return False # Không có trường nào hợp lệ để update

        values.append(user_id) # Tham số cuối cùng cho WHERE id = %s

        query = f"UPDATE Employee SET {', '.join(set_clauses)} WHERE id = %s"
        
        # db.execute_query trả về số dòng bị ảnh hưởng hoặc True/False tùy thư viện bạn dùng
        return db.execute_query(query, tuple(values))