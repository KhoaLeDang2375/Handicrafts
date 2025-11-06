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
        INSERT INTO Customers (name, address, email, user_name,  password)
        VALUES (%s, %s, %s, %s, %s)
        """
        return db.execute_query(query, (self.name, self.address, self.email, self.username,  self.password))

    @staticmethod
    def get_by_id(user_id):
        query = "SELECT * FROM Customers WHERE id = %s"
        return db.fetch_one(query, (user_id,))

    @staticmethod
    def get_by_email(email):
        query = "SELECT * FROM Customers WHERE email = %s"
        return db.fetch_one(query, (email,))