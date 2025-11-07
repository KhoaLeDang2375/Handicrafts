from app.database.database import db
from datetime import datetime

class Payment:
    def __init__(self, payment_method='COD', status='Pending'):
        self.payment_method = payment_method
        self.status = status
        self.payment_date = None

    def save(self):
        query = """
        INSERT INTO Payment (payment_method, status, payment_date)
        VALUES (%s, %s, %s)
        """
        return db.execute_query(query, (
            self.payment_method,
            self.status,
            self.payment_date
        ))

    @staticmethod
    def get_by_id(payment_id):
        query = """SELECT * FROM Payment WHERE id = %s"""
        return db.fetch_one(query, (payment_id,))

    def update_status(self, payment_id, status):
        payment_date = datetime.now() if status == 'Paid' else None
        query = """
        UPDATE Payment 
        SET status = %s, payment_date = %s 
        WHERE id = %s
        """
        return db.execute_query(query, (status, payment_date, payment_id))

    @staticmethod
    def get_all_by_status(status):
        query = """SELECT * FROM Payment WHERE status = %s"""
        return db.fetch_all(query, (status,))