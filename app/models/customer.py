from app.database import db

class Customer:
    def __init__(self, name, address, email, phone, username, password):
        self.name = name
        self.address = address
        self.email = email
        self.phone = phone
        self.username = username
        self.password = password

    def save(self):
        query = """
        INSERT INTO Customers (name, address, email, user_name,  password, phone)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        return db.execute_query(query, (self.name, self.address, self.email, self.username,  self.password, self.phone))

    @staticmethod
    def get_by_id(user_id):
        query = "SELECT name, address, email, phone, user_name FROM Customers WHERE id = %s"
        return db.fetch_one(query, (user_id,))

    @staticmethod
    def get_by_email(email):
        query = "SELECT name, address, email, phone, user_name FROM Customers WHERE email = %s"
        return db.fetch_one(query, (email,))
    @staticmethod
    def get_by_username(username):
        # Return full user record including id and password so login can verify credentials
        query = "SELECT * FROM Customers WHERE user_name = %s"
        return db.fetch_one(query, (username,))
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

        query = f"UPDATE Customers SET {', '.join(set_clauses)} WHERE id = %s"
        
        # db.execute_query trả về số dòng bị ảnh hưởng hoặc True/False tùy thư viện bạn dùng
        return db.execute_query(query, tuple(values))