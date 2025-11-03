from app.database import db
from datetime import datetime

class Review:
    def __init__(self, customer_id, variant_id, rating, content):
        self.customer_id = customer_id
        self.variant_id = variant_id
        self.rating = rating
        self.content = content
        self.date = datetime.now()

    def save(self):
        query = """
        INSERT INTO reviews (customer_id, variant_id, rating, content, date)
        VALUES (%s, %s, %s, %s, %s)
        """
        return db.execute_query(query, (
            self.customer_id,
            self.variant_id,
            self.rating,
            self.content,
            self.date
        ))

    @staticmethod
    def get_by_id(review_id):
        query = """
        SELECT r.*, c.name as customer_name, p.name as product_name
        FROM reviews r
        JOIN customers c ON r.customer_id = c.id
        JOIN ProductVariant pv ON r.variant_id = pv.id
        JOIN products p ON pv.product_id = p.id
        WHERE r.id = %s
        """
        return db.fetch_one(query, (review_id,))

    @staticmethod
    def get_by_product_variant(variant_id):
        query = """
        SELECT r.*, c.name as customer_name
        FROM reviews r
        JOIN customers c ON r.customer_id = c.id
        WHERE r.variant_id = %s
        ORDER BY r.date DESC
        """
        return db.fetch_all(query, (variant_id,))

    @staticmethod
    def get_average_rating(variant_id):
        query = """
        SELECT AVG(rating) as average_rating
        FROM reviews
        WHERE variant_id = %s
        """
        return db.fetch_one(query, (variant_id,))