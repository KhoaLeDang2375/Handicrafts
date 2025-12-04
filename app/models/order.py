# from app.database import db
# from datetime import datetime

# class Order:
#     def __init__(self, user_id, amount, status='pending'):
#         self.user_id = user_id
#         self.total_amount = amount
#         self.status = status
#         self.created_at = datetime.now()

#     def save(self):
#         query = """
#         INSERT INTO Orders (customer_id, amount, status, date)
#         VALUES (%s, %s, %s, %s)
#         """
#         result = db.execute_query(query, (
#             self.user_id,
#             self.total_amount,
#             self.status,
#             self.created_at
#         ))
#         # If an insert produced a lastrowid, store it on the instance for callers
#         try:
#             if isinstance(result, int) and result > 0:
#                 self.id = result
#         except Exception:
#             pass
#         return result

#     @staticmethod
#     def get_by_id(order_id):
#         query = """SELECT * FROM Orders WHERE id = %s"""
#         return db.fetch_one(query, (order_id,))

#     @staticmethod
#     def get_user_orders(user_id, limit=None, offset=None):
#         query = """SELECT * FROM Orders WHERE user_id = %s ORDER BY created_at DESC"""
#         params = [user_id]
#         if limit is not None:
#             query += " LIMIT %s"
#             params.append(limit)
#         if offset is not None:
#             query += " OFFSET %s"
#             params.append(offset)
#         return db.fetch_all(query, tuple(params))

#     def update_status(self, order_id, new_status):
#         query = """
#         UPDATE Orders
#         SET status = %s, updated_at = NOW()
#         WHERE id = %s
#         """
#         return db.execute_query(query, (new_status, order_id))

from app.database import db
from datetime import datetime

class Order:
    # 1. Cập nhật __init__ để nhận thêm shipping_name, phone, address
    def __init__(self, customer_id, amount, status, shipping_name, shipping_phone, shipping_address, id=None, employee_id=None):
        self.id = id
        self.customer_id = customer_id
        self.employee_id = employee_id
        self.amount = amount
        self.status = status
        self.created_at = datetime.now()
        
        # Các trường mới thêm
        self.shipping_name = shipping_name
        self.shipping_phone = shipping_phone
        self.shipping_address = shipping_address
        

    # 2. Cập nhật hàm save để INSERT vào database
    def save(self):
        # Đảm bảo bảng 'orders' trong MySQL đã có đủ cột (shipping_name...)
        sql = """
            INSERT INTO orders 
            (customer_id, amount, status, shipping_name, shipping_phone, shipping_address) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            self.customer_id, 
            self.amount, 
            self.status, 
            self.shipping_name, 
            self.shipping_phone, 
            self.shipping_address, 
        )
        
        # Thực thi và lấy ID vừa tạo
        new_id = db.execute_query(sql, params)
        self.id = new_id
        return new_id

    # 3. Các hàm hỗ trợ khác (Giữ nguyên hoặc cập nhật nếu cần)
    @staticmethod
    def get_by_id(order_id):
        sql = "SELECT * FROM orders WHERE id = %s"
        return db.fetch_one(sql, (order_id,))

    @staticmethod
    def get_user_orders(customer_id):
        sql = "SELECT * FROM orders WHERE user_id = %s ORDER BY date DESC"
        return db.fetch_all(sql, (customer_id,))
    
    @staticmethod
    def update_amount(order_id, amount):
        sql = "UPDATE orders SET amount = %s WHERE id = %s"
        return db.execute_query(sql, (amount, order_id))
    
    def update_status(self, order_id, new_status):
        sql = "UPDATE orders SET status = %s WHERE id = %s"
        return db.execute_query(sql, (new_status, order_id))
    
    @staticmethod
    def get_by_customer_id(user_id):
         sql = "SELECT * FROM orders WHERE user_id = %s ORDER BY date DESC"
         return db.fetch_all(sql, (user_id,))