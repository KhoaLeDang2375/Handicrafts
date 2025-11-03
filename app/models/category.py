from app.database import db

class Category: 
    def __init__(self, name):
        self.name = name
    def save(self):
        query = """
        INSERT INTO categories (name)
        VALUES (%s)
        """     
        return db.execute_query(query,(self.name,))
    @staticmethod
    def get_category_by_id(id):
        query = """SELECT * FROM categories WHERE id = %s"""
        return db.fetch_one(query, (id,))
    
    @staticmethod
    def get_all():
        query = """SELECT * FROM categories"""
        return db.fetch_all(query)