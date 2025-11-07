from app.database.database import db

class ProductVariant:
    def __init__(self, product_id, color, size, price, amount):
        self.product_id = product_id
        self.color = color
        self.size = size
        self.price = price
        self.amount = amount

    def save(self):
        query = """
        INSERT INTO ProductVariant (product_id, color, size, price, amount)
        VALUES (%s, %s, %s, %s, %s)
        """
        return db.execute_query(query, (
            self.product_id,
            self.color,
            self.size,
            self.price,
            self.amount
        ))

    @staticmethod
    def get_by_id(variant_id):
        query = """
        SELECT v.*, p.name as product_name 
        FROM ProductVariant v
        JOIN products p ON v.product_id = p.id
        WHERE v.id = %s
        """
        return db.fetch_one(query, (variant_id,))

    @staticmethod
    def get_by_product(product_id, variant_id = None, get_one = False):
        if get_one:
             query = """
                    SELECT * FROM ProductVariant 
                    WHERE product_id = %s and id = %s
                    LIMIT 1;
                    """
             return db.fetch_one(query,(product_id,variant_id))
        else:
            query = """
            SELECT * FROM ProductVariant
            WHERE product_id = %s
            """
            return db.fetch_all(query, (product_id,))
    def update_stock(self, variant_id, amount):
        query = """
        UPDATE ProductVariant 
        SET amount = amount + %s 
        WHERE id = %s
        """
        return db.execute_query(query, (amount, variant_id))

    def update_price(self, variant_id, price):
        query = """
        UPDATE ProductVariant 
        SET price = %s 
        WHERE id = %s
        """
        return db.execute_query(query, (price, variant_id))