from app.database import db

class OrderDetail:
    def __init__(self, order_id, variant_id, product_quantity, price):
        self.order_id = order_id
        self.variant_id = variant_id
        self.product_quantity = product_quantity
        self.price = price
        self.subtotal = product_quantity * price

    def save(self):
        query = """
        INSERT INTO OrderDetail (order_id, variant_id, product_quantity, price, subtotal)
        VALUES (%s, %s, %s, %s, %s)
        """
        return db.execute_query(query, (
            self.order_id,
            self.variant_id,
            self.product_quantity,
            self.price,
            self.subtotal
        ))

    @staticmethod
    def get_order_items(order_id):
        query = """
        SELECT od.*, p.name as product_name, p.image_url
        FROM OrderDetail od
        JOIN Products p ON od.variant_id = p.id
        WHERE od.order_id = %s
        """
        return db.fetch_all(query, (order_id,))

    @staticmethod
    def get_product_sales(variant_id):
        query = """
        SELECT SUM(product_quantity) as total_sold, SUM(subtotal) as total_revenue
        FROM OrderDetail
        WHERE variant_id = %s
        """
        return db.fetch_one(query, (variant_id,))