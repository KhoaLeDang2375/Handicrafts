from app.database import db
from datetime import datetime
from typing import Optional

class Review:
    def __init__(self, customer_id, variant_id, rating, content):
        self.customer_id = customer_id
        self.variant_id = variant_id
        self.rating = rating
        self.content = content
        self.date = datetime.now()
        
    @staticmethod
    def format_datetime(dt: Optional[datetime]) -> Optional[str]:
        """Convert datetime to ISO format string or return None"""
        return dt.isoformat() if dt else None
    @staticmethod
    def check_user_buy_item(customer_id: int, variant_id: int) -> bool:
        # Original query for validation
        query = """
        SELECT EXISTS (
            SELECT 1
            FROM Orders o
            INNER JOIN OrderDetail od ON o.id = od.order_id
            WHERE 
                o.customer_id = %s
                AND od.variant_id = %s
                AND o.status = 'received'
        ) as has_bought
        """
        result = db.fetch_one(query, (customer_id, variant_id))
        return bool(result['has_bought']) if result else False
    def save(self):
        query = """
        INSERT INTO Reviews (customer_id, variant_id, rating, content, date)
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
        FROM Reviews r
        JOIN Customers c ON r.customer_id = c.id
        JOIN ProductVariant pv ON r.variant_id = pv.id
        JOIN Products p ON pv.product_id = p.id
        WHERE r.id = %s
        """
        result = db.fetch_one(query, (review_id,))
        if result and 'date' in result and isinstance(result['date'], datetime):
            result['date'] = result['date'].isoformat()
        return result

    @staticmethod
    def get_by_product_variant(variant_id):
        query = """
        SELECT r.*, c.name as customer_name
        FROM Reviews r
        JOIN Customers c ON r.customer_id = c.id
        WHERE r.variant_id = %s
        ORDER BY r.date DESC
        """
        results = db.fetch_all(query, (variant_id,))
        for r in results:
            if 'date' in r and isinstance(r['date'], datetime):
                r['date'] = r['date'].isoformat()
        return results

    @staticmethod
    def get_average_rating(variant_id):
        query = """
        SELECT AVG(rating) as average_rating
        FROM Reviews
        WHERE variant_id = %s
        """
        return db.fetch_one(query, (variant_id,))

    @staticmethod
    def update(review_id, rating=None, content=None):
        updates = []
        params = []
        if rating is not None:
            updates.append("rating = %s")
            params.append(rating)
        if content is not None:
            updates.append("content = %s")
            params.append(content)
        if not updates:
            return False
        # update date to now
        updates.append("date = %s")
        params.append(datetime.now())
        params.append(review_id)
        query = f"""
        UPDATE Reviews SET {', '.join(updates)} WHERE id = %s
        """
        return db.execute_query(query, tuple(params))

    @staticmethod
    def delete(review_id):
        query = """
        DELETE FROM Reviews WHERE id = %s
        """
        return db.execute_query(query, (review_id,))

    @staticmethod
    def count_by_variant(variant_id):
        query = """
        SELECT COUNT(*) as total FROM Reviews WHERE variant_id = %s
        """
        result = db.fetch_one(query, (variant_id,))
        return result['total'] if result else 0