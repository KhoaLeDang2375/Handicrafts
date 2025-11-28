# from app.database import db

# class Cart:
#     def __init__(self, user_id, productvariant_id, quantity):
#         self.user_id = user_id
#         self.productvariant_id = productvariant_id
#         self.quantity = quantity
#         self._calculate_total_price()

#     def _calculate_total_price(self):
#         query = """
#         SELECT price FROM ProductVariant WHERE id = %s
#         """
#         result = db.fetch_one(query, (self.productvariant_id,))
#         self.total_price = result['price'] * self.quantity if result else 0

#     def save(self):
#         # Kiểm tra xem sản phẩm đã có trong giỏ hàng chưa
#         existing = self.get_item(self.user_id, self.productvariant_id)
#         if existing:
#             return self.update_quantity(
#                 existing['id'], 
#                 existing['quantity'] + self.quantity
#             )

#         query = """
#         INSERT INTO Cart (user_id, productvariant_id, quantity, total_price)
#         VALUES (%s, %s, %s, %s)
#         """
#         return db.execute_query(query, (
#             self.user_id,
#             self.productvariant_id,
#             self.quantity,
#             self.total_price
#         ))

#     @staticmethod
#     def get_user_cart(user_id):
#         query = """
#         SELECT c.*, 
#                pv.color, pv.size, pv.price,
#                p.name as product_name
#         FROM Cart c
#         JOIN ProductVariant pv ON c.productvariant_id = pv.id
#         JOIN Products p ON pv.product_id = p.id
#         WHERE c.user_id = %s
#         """
#         return db.fetch_all(query, (user_id,))

#     @staticmethod
#     def get_item(user_id, productvariant_id):
#         query = """
#         SELECT * FROM Cart 
#         WHERE user_id = %s AND productvariant_id = %s
#         """
#         return db.fetch_one(query, (user_id, productvariant_id))

#     def update_quantity(self, variant_id, quantity):
#         self.quantity = quantity
#         self._calculate_total_price()
#         query = """
#         UPDATE Cart 
#         SET quantity = %s, total_price = %s 
#         WHERE user_id = %s AND productvariant_id = %s
#         """
#         return db.execute_query(query, (
#             self.quantity,
#             self.total_price,
#             self.user_id,
#             variant_id
#         ))
#     @staticmethod
#     def update_item_quantity(user_id, variant_id, quantity):
#         query = """
#         UPDATE Cart 
#         SET quantity = %s, total_price = 
#             (SELECT price FROM ProductVariant WHERE id = %s) * %s
#         WHERE user_id = %s AND productvariant_id = %s
#         """
#         return db.execute_query(query, (
#             quantity,
#             variant_id,
#             quantity,
#             user_id,
#             variant_id
#         ))
#     @staticmethod
#     def remove_item(variant_id):
#         query = """DELETE FROM Cart WHERE productvariant_id = %s"""
#         return db.execute_query(query, (variant_id,))

#     @staticmethod
#     def clear_cart(user_id):
#         query = """DELETE FROM Cart WHERE user_id = %s"""
#         return db.execute_query(query, (user_id,))

#     @staticmethod
#     def get_cart_total(user_id):
#         query = """
#         SELECT SUM(total_price) as cart_total 
#         FROM Cart 
#         WHERE user_id = %s
#         """
#         result = db.fetch_one(query, (user_id,))
#         return result['cart_total'] if result else 0

from app.database import db

class Cart:
    def __init__(self, user_id, productvariant_id, quantity, total_price=0):
        self.user_id = user_id
        self.productvariant_id = productvariant_id
        self.quantity = quantity
        self.total_price = total_price
        
        # Nếu lúc khởi tạo chưa có giá, phải tính ngay để chuẩn bị lưu vào DB
        if self.total_price == 0:
            self._calculate_total_price()

    def _calculate_total_price(self):
        """Lấy giá từ bảng productVariant để tính tổng"""
        # CHÚ Ý: Tên bảng là productVariant 
        query = "SELECT price FROM productVariant WHERE id = %s"
        result = db.fetch_one(query, (self.productvariant_id,))
        
        # Nếu tìm thấy variant thì nhân giá, không thì bằng 0
        if result:
            self.total_price = float(result['price']) * int(self.quantity)
        else:
            self.total_price = 0

    def save(self):
        # 1. Kiểm tra xem món này đã có trong giỏ chưa
        existing = self.check_item_exists(self.user_id, self.productvariant_id)
        
        if existing:
            # Nếu có rồi -> Cộng dồn số lượng
            new_quantity = existing['quantity'] + self.quantity
            return self.update_item_quantity(self.user_id, self.productvariant_id, new_quantity)

        # 2. Nếu chưa có -> INSERT mới
        # Lưu ý: Lưu cả total_price vào bảng cart theo ý bạn
        sql = """
            INSERT INTO cart (user_id, productvariant_id, quantity, total_price)
            VALUES (%s, %s, %s, %s)
        """
        return db.execute_query(sql, (
            self.user_id, 
            self.productvariant_id, 
            self.quantity, 
            self.total_price
        ))

    @staticmethod
    def get_user_cart(user_id):
        """
        Lấy giỏ hàng.
        JOIN với bảng 'productVariant' và 'products'.
        """
        sql = """
            SELECT 
                c.id, 
                c.user_id, 
                c.productvariant_id, 
                c.quantity,
                c.total_price,
                pv.price, 
                pv.color, 
                pv.size,
                p.id as product_id,
                p.name as product_name
            FROM cart c
            JOIN productVariant pv ON c.productvariant_id = pv.id
            JOIN products p ON pv.product_id = p.id
            WHERE c.user_id = %s
        """
        return db.fetch_all(sql, (user_id,))

    @staticmethod
    def check_item_exists(user_id, productvariant_id):
        sql = "SELECT * FROM cart WHERE user_id = %s AND productvariant_id = %s"
        return db.fetch_one(sql, (user_id, productvariant_id))

    @staticmethod
    def update_item_quantity(user_id, variant_id, new_quantity):
        """
        Cập nhật số lượng VÀ cập nhật luôn total_price
        """
        sql = """
        UPDATE cart 
        SET quantity = %s,
            total_price = (SELECT price FROM productVariant WHERE id = %s) * %s
        WHERE user_id = %s AND productvariant_id = %s
        """
        return db.execute_query(sql, (
            new_quantity, 
            variant_id,   # Tham số cho subquery lấy giá
            new_quantity, # Tham số để nhân
            user_id, 
            variant_id
        ))

    @staticmethod
    def remove_item(user_id, variant_id):
        sql = "DELETE FROM cart WHERE user_id = %s AND productvariant_id = %s"
        return db.execute_query(sql, (user_id, variant_id))

    @staticmethod
    def clear_cart(user_id):
        sql = "DELETE FROM cart WHERE user_id = %s"
        return db.execute_query(sql, (user_id,))