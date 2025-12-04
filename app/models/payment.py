from app.database import db
from datetime import datetime

class Payment:
    def __init__(self, order_id, payment_method='COD', status='Pending', payment_date=None):
        self.order_id = order_id
        self.payment_method = payment_method
        self.status = status
        self.payment_date = payment_date
 
    def save(self):
        query = """
        INSERT INTO Payment (order_id, payment_method, status, payment_date)
        VALUES (%s, %s, %s, %s)
        """

        return db.execute_query(query, (
            self.order_id,
            self.payment_method,
            self.status,
            self.payment_date
        ))

    @staticmethod
    def get_by_id(payment_id):
        query = """SELECT * FROM Payment WHERE id = %s"""
        return db.fetch_one(query, (payment_id,))
   
    def update_status(self, payment_id, status):
        payment_date = datetime.now() if status.lower() == 'Paid' else None
        query = """
        UPDATE Payment
        SET status = %s, payment_date = IFNULL(%s, payment_date)
        WHERE id = %s
        """
        return db.execute_query(query, (status, payment_date, payment_id))

    @staticmethod
    def get_all_by_status(status):
        query = """SELECT * FROM Payment WHERE status = %s"""
        return db.fetch_all(query, (status,))
    
    # Thêm hàm tìm payment theo order_id (Rất cần thiết khi xem chi tiết đơn hàng)
    @staticmethod
    def get_by_order_id(order_id):
        query = "SELECT * FROM payment WHERE order_id = %s"
        return db.fetch_one(query, (order_id,))
