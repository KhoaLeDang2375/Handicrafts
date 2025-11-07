from app.database.database import db

class Cart:
    def __init__(self, user_id, productvariant_id, quantity):
        self.user_id = user_id
        self.productvariant_id = productvariant_id
        self.quantity = quantity
        self._calculate_total_price()

    def _calculate_total_price(self):
        query = """
        SELECT price FROM ProductVariant WHERE id = %s
        """
        result = db.fetch_one(query, (self.productvariant_id,))
        self.total_price = result['price'] * self.quantity if result else 0

    def save(self):
        # Kiểm tra xem sản phẩm đã có trong giỏ hàng chưa
        existing = self.get_item(self.user_id, self.productvariant_id)
        if existing:
            return self.update_quantity(
                existing['id'], 
                existing['quantity'] + self.quantity
            )

        query = """
        INSERT INTO Cart (user_id, productvariant_id, quantity, total_price)
        VALUES (%s, %s, %s, %s)
        """
        return db.execute_query(query, (
            self.user_id,
            self.productvariant_id,
            self.quantity,
            self.total_price
        ))

    @staticmethod
    def get_user_cart(user_id):
        query = """
        SELECT c.*, 
               pv.color, pv.size, pv.price,
               p.name as product_name
        FROM Cart c
        JOIN ProductVariant pv ON c.productvariant_id = pv.id
        JOIN products p ON pv.product_id = p.id
        WHERE c.user_id = %s
        """
        return db.fetch_all(query, (user_id,))

    @staticmethod
    def get_item(user_id, productvariant_id):
        query = """
        SELECT * FROM Cart 
        WHERE user_id = %s AND productvariant_id = %s
        """
        return db.fetch_one(query, (user_id, productvariant_id))

    def update_quantity(self, cart_id, quantity):
        self.quantity = quantity
        self._calculate_total_price()
        
        query = """
        UPDATE Cart 
        SET quantity = %s, total_price = %s 
        WHERE id = %s
        """
        return db.execute_query(query, (quantity, self.total_price, cart_id))

    @staticmethod
    def remove_item(cart_id):
        query = """DELETE FROM Cart WHERE id = %s"""
        return db.execute_query(query, (cart_id,))

    @staticmethod
    def clear_cart(user_id):
        query = """DELETE FROM Cart WHERE user_id = %s"""
        return db.execute_query(query, (user_id,))

    @staticmethod
    def get_cart_total(user_id):
        query = """
        SELECT SUM(total_price) as cart_total 
        FROM Cart 
        WHERE user_id = %s
        """
        result = db.fetch_one(query, (user_id,))
        return result['cart_total'] if result else 0