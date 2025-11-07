from app.database import db
from datetime import datetime

class Blog:
    def __init__(self, author_id, content):
        self.author_id = author_id
        self.content = content
        self.create_time = datetime.now()

    def save(self):
        query = """
        INSERT INTO Blog (author_id, content, create_time, author_name)
        VALUES (%s, %s, %s, %s)
        """
        return db.execute_query(query, (
            self.author_id,
            self.content,
            self.create_time,
            self.author_name
        ))

    @staticmethod
    def get_by_id(blog_id):
        query = """
        SELECT b.*, e.name as author_name
        FROM Blog b
        JOIN Employee e ON b.author_id = e.id
        WHERE b.id = %s
        """
        return db.fetch_one(query, (blog_id,))

    @staticmethod
    def get_all(skip: int = 0, limit: int = 100):
        query = """
        SELECT b.*, e.name as author_name
        FROM Blog b
        JOIN Employee e ON b.author_id = e.id
        ORDER BY b.create_time DESC
        LIMIT %s OFFSET %s
        """
        return db.fetch_all(query, (limit, skip))

    @staticmethod
    def get_by_author(author_id):
        query = """
        SELECT * FROM Blog 
        WHERE author_id = %s
        ORDER BY create_time DESC
        """
        return db.fetch_all(query, (author_id,))

    def update_content(self, blog_id, content):
        query = """
        UPDATE Blog 
        SET content = %s 
        WHERE id = %s
        """
        return db.execute_query(query, (content, blog_id))