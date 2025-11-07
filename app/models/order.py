from app.database.database import db
from datetime import datetime

class Order:
    def __init__(self, user_id, total_amount, status='pending'):
        self.user_id = user_id
        self.total_amount = total_amount
        self.status = status
        self.created_at = datetime.now()

    def save(self):
        query = """
        INSERT INTO orders (user_id, total_amount, status, created_at)
        VALUES (%s, %s, %s, %s)
        """
        return db.execute_query(query, (
            self.user_id,
            self.total_amount,
            self.status,
            self.created_at
        ))

    @staticmethod
    def get_by_id(order_id):
        query = """SELECT * FROM orders WHERE id = %s"""
        return db.fetch_one(query, (order_id,))

    @staticmethod
    def get_user_orders(user_id):
        query = """SELECT * FROM orders WHERE user_id = %s ORDER BY created_at DESC"""
        return db.fetch_all(query, (user_id,))

    def update_status(self, order_id, new_status):
        query = """
        UPDATE orders 
        SET status = %s, updated_at = NOW()
        WHERE id = %s
        """
        return db.execute_query(query, (new_status, order_id))