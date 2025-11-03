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
        INSERT INTO products (id,name, description, category_id, status, artisan_description)
        VALUES ( %s, %s, %s, %s, %s)
        """
        return db.execute_query(query, (
            self.name, 
            self.description, 
            self.category_id,
            self.status,
            self.artisan_description
        ))
    
    @staticmethod
    def get_all():
        query = """
        SELECT 
            p.id,
            p.name,
            p.description,
            p.category_id,
            p.status,
            p.artisan_description,
            c.name as category_name
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        """
        return db.fetch_all(query)

    @staticmethod
    def get_by_id(product_id):
        query = """
        SELECT 
            p.name,
            p.description,
            p.category_id,
            p.status,
            p.artisan_description,
            c.name as category_name
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        WHERE p.id = %s
        """
        return db.fetch_one(query, (product_id,))
        
    @staticmethod
    def get_by_category(category_id):
        query = """
        SELECT 
            p.name,
            p.description,
            p.category_id,
            p.status,
            p.artisan_description,
            c.name as category_name
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        WHERE p.category_id = %s
        """
        return db.fetch_all(query, (category_id,))
