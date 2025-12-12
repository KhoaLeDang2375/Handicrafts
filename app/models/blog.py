from app.database import db
from datetime import datetime

class Blog:
    def __init__(self, author_id: int, content: str, title, author_name: str = None):
        self.author_id = author_id
        self.content = content
        self.title = title
        self.author_name = author_name
        self.create_time = datetime.utcnow()  

    def save(self):
        """
        Lưu một bài viết mới vào cơ sở dữ liệu.
        """
        query = """
        INSERT INTO Blog (author_id, content, title, create_time, author_name)
        VALUES (%s, %s, %s, %s, %s)
        """
        return db.execute_query(query, (
            self.author_id,
            self.content,
            self.title,
            self.create_time,
            self.author_name
        ))

    # -------------------------------
    # STATIC METHODS
    # -------------------------------
    @staticmethod
    def get_by_id(blog_id: int):
        """
        Lấy chi tiết một bài viết theo ID.
        """
        query = """
        SELECT 
            b.id,
            b.author_id,
            e.name AS author_name,
            b.title,   -- <--- QUAN TRỌNG: Đã thêm title
            b.content,
            b.create_time
        FROM Blog b
        JOIN Employee e ON b.author_id = e.id
        WHERE b.id = %s
        """
        return db.fetch_one(query, (blog_id,))

    @staticmethod
    def get_all(skip: int = 0, limit: int = 10):
        """
        Lấy danh sách blog (phân trang).
        """
        query = """
        SELECT 
            b.id,
            b.author_id,
            e.name AS author_name,
            b.title,
            b.content,
            b.create_time
        FROM Blog b
        JOIN Employee e ON b.author_id = e.id
        ORDER BY b.create_time DESC
        LIMIT %s OFFSET %s
        """
        return db.fetch_all(query, (limit, skip))

    @staticmethod
    def get_by_author(author_id: int, skip: int = 0, limit: int = 10):
        """
        Lấy danh sách bài viết của một tác giả (phân trang).
        """
        query = """
        SELECT 
            b.id,
            b.author_id,
            e.name AS author_name,
            b.title,   -- <--- QUAN TRỌNG: Đã thêm title
            b.content,
            b.create_time
        FROM Blog b
        JOIN Employee e ON b.author_id = e.id
        WHERE b.author_id = %s
        ORDER BY b.create_time DESC
        LIMIT %s OFFSET %s
        """
        return db.fetch_all(query, (author_id, limit, skip))

    @staticmethod
    def update_content(blog_id: int, title: str, content: str):
        """
        Cập nhật tiêu đề và nội dung bài viết.
        """
        # --- SỬA LOGIC UPDATE: Nhận cả title và content ---
        query = """
        UPDATE Blog
        SET title = %s, content = %s
        WHERE id = %s
        """
        return db.execute_query(query, (title, content, blog_id))

    @staticmethod
    def delete(blog_id: int):
        """
        Xóa bài viết khỏi cơ sở dữ liệu.
        """
        query = "DELETE FROM Blog WHERE id = %s"
        return db.execute_query(query, (blog_id,))

    @staticmethod
    def count_all():
        query = "SELECT COUNT(*) AS total FROM Blog"
        result = db.fetch_one(query)
        return result["total"] if result else 0

    @staticmethod
    def count_by_author(author_id: int):
        query = "SELECT COUNT(*) AS total FROM Blog WHERE author_id = %s"
        result = db.fetch_one(query, (author_id,))
        return result["total"] if result else 0