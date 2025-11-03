from app.database import db

class OrderDetail:
    def __init__(self, order_id, product_id, quantity, price):
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price
        self.subtotal = quantity * price

    def save(self):
        query = """
        INSERT INTO order_details (order_id, product_id, quantity, price, subtotal)
        VALUES (%s, %s, %s, %s, %s)
        """
        return db.execute_query(query, (
            self.order_id,
            self.product_id,
            self.quantity,
            self.price,
            self.subtotal
        ))

    @staticmethod
    def get_order_items(order_id):
        query = """
        SELECT od.*, p.name as product_name, p.image_url
        FROM order_details od
        JOIN products p ON od.product_id = p.id
        WHERE od.order_id = %s
        """
        return db.fetch_all(query, (order_id,))

    @staticmethod
    def get_product_sales(product_id):
        query = """
        SELECT SUM(quantity) as total_sold, SUM(subtotal) as total_revenue
        FROM order_details
        WHERE product_id = %s
        """
        return db.fetch_one(query, (product_id,))