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
    # Nhận thêm shipping_name, phone, address
    def __init__(self, customer_id, amount, status, shipping_name, shipping_phone, shipping_address, id=None, employee_id=None, date=None):
        self.id = id
        self.customer_id = customer_id
        self.employee_id = employee_id
        self.amount = amount
        self.status = status
        self.date = datetime.now()
        
        # Các trường mới thêm
        self.shipping_name = shipping_name
        self.shipping_phone = shipping_phone
        self.shipping_address = shipping_address
        
    def save(self):
        sql = """
            INSERT INTO orders 
            (customer_id, amount, status, shipping_name, shipping_phone, shipping_address, date) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            self.customer_id, 
            self.amount, 
            self.status, 
            self.shipping_name, 
            self.shipping_phone, 
            self.shipping_address, 
            self.date
        )
        
        # Thực thi và lấy ID vừa tạo
        new_id = db.execute_query(sql, params)
        self.id = new_id
        return new_id

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
    
    @staticmethod
    def get_orders_by_customer(customer_id, status=None):
        sql = """
            SELECT 
                o.id, 
                o.status, 
                o.date, 
                o.amount, 
                COALESCE(SUM(od.product_quantity), 0) as total_products
            FROM orders o
            LEFT JOIN orderdetail od ON o.id = od.order_id
            WHERE o.customer_id = %s
        """
        params = [customer_id]

        # Xử lý logic cộng chuỗi SQL (Dynamic SQL)
        if status:
            sql += " AND o.status = %s"
            params.append(status)

        sql += " GROUP BY o.id, o.status, o.date, o.amount ORDER BY o.date DESC"

        # db.fetch_all sẽ trả về list các tuple [(id, status, ...), (...)]
        rows = db.fetch_all(sql, tuple(params))
        
        # Map dữ liệu từ Tuple sang Dictionary
        result = []
        if rows:
            for row in rows:
                result.append({
                    "order_id": row['id'],            
                    "status": row['status'],           
                    "date": row['date'],         
                    "total_amount": row['amount'],     
                    "total_products": int(row['total_products']) 
                })
                
        return result