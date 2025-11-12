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