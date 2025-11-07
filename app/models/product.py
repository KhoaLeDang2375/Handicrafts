from app.database import db
from datetime import datetime

class Product:
    def __init__(self, name, description,category_id,  status, artisan_description):
        self.name = name
        self.description = description
        self.category_id = category_id
        self.status = status
        self.artisan_description =artisan_description
    def save(self):
        query = """
        INSERT INTO Products (name, description, category_id, status, artisan_description)
        VALUES (%s, %s, %s, %s, %s)
        """
        return db.execute_query(query, (
            self.name, 
            self.description, 
            self.category_id,
            self.status,
            self.artisan_description
        ))
    
    @staticmethod
    def get_all(skip=0, limit=10):
        query = """
        SELECT 
            p.id,
            p.name,
            p.description,
            p.category_id,
            p.status,
            p.artisan_description,
            c.name as category_name,
            c.id as category_id
        FROM Products p
        LEFT JOIN Categories c ON p.category_id = c.id
        LIMIT %s OFFSET %s
        """
        return db.fetch_all(query, (limit, skip))
        
    @staticmethod
    def count_all():
        query = """
        SELECT COUNT(*) as total
        FROM Products
        """
        result = db.fetch_one(query)
        return result['total'] if result else 0

    @staticmethod
    def get_by_id(product_id):
        query = """
        SELECT 
            p.id,
            p.name,
            p.description,
            p.category_id AS product_category_id,
            p.status,
            p.artisan_description,
            c.name AS category_name,
            c.id AS category_id,
            JSON_OBJECT(
                'id', c.id,
                'name', c.name
            ) AS category
        FROM Products p
        LEFT JOIN Categories c ON p.category_id = c.id
        WHERE p.id = %s;
        """
        return db.fetch_one(query, (product_id,))
        
    @staticmethod
    def get_by_category(category_id, skip=0, limit=10):
        query = """
        SELECT 
            p.id,
            p.name,
            p.description,
            p.category_id,
            p.status,
            p.artisan_description,
            c.name as category_name,
            c.id as category_id
        FROM Products p
        LEFT JOIN Categories c ON p.category_id = c.id
        WHERE p.category_id = %s
        ORDER BY p.id
        LIMIT %s OFFSET %s
        """
        return db.fetch_all(query, (category_id, limit, skip))
        
    @staticmethod
    def count_by_category(category_id):
        query = """
        SELECT COUNT(*) as total
        FROM Products
        WHERE category_id = %s
        """
        result = db.fetch_one(query, (category_id,))
        return result['total'] if result else 0
