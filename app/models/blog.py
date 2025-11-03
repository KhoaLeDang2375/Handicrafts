from app.database import db
from datetime import datetime

class Blog:
    def __init__(self, author_id, content):
        self.author_id = author_id
        self.content = content
        self.create_time = datetime.now()

    def save(self):
        query = """
        INSERT INTO Blog (Author_id, Content, create_time)
        VALUES (%s, %s, %s)
        """
        return db.execute_query(query, (
            self.author_id,
            self.content,
            self.create_time
        ))

    @staticmethod
    def get_by_id(blog_id):
        query = """
        SELECT b.*, e.name as author_name
        FROM Blog b
        JOIN Employee e ON b.Author_id = e.id
        WHERE b.id = %s
        """
        return db.fetch_one(query, (blog_id,))

    @staticmethod
    def get_all():
        query = """
        SELECT b.*, e.name as author_name
        FROM Blog b
        JOIN Employee e ON b.Author_id = e.id
        ORDER BY b.create_time DESC
        """
        return db.fetch_all(query)

    @staticmethod
    def get_by_author(author_id):
        query = """
        SELECT * FROM Blog 
        WHERE Author_id = %s
        ORDER BY create_time DESC
        """
        return db.fetch_all(query, (author_id,))

    def update_content(self, blog_id, content):
        query = """
        UPDATE Blog 
        SET Content = %s 
        WHERE id = %s
        """
        return db.execute_query(query, (content, blog_id))