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

    def update(self, employee_id, **kwargs):
        fields = []
        values = []
        for key, value in kwargs.items():
            fields.append(f"{key} = %s")
            values.append(value)
        values.append(employee_id)
        
        query = f"""
        UPDATE Employee 
        SET {', '.join(fields)}
        WHERE id = %s
        """
        return db.execute_query(query, tuple(values))