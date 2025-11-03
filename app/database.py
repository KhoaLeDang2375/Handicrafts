import os
import pymysql
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

class Database:
    def __init__(self):
        self.host = os.getenv('DB_HOST')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.db = os.getenv('DB_NAME')
        self.connection = None
        self.cursor = None

    def connect(self):
        """Thiết lập kết nối với database"""
        try:
            if not self.connection:
                self.connection = pymysql.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    db=self.db,
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor
                )
                self.cursor = self.connection.cursor()
                print("Kết nối database thành công!")
        except Exception as e:
            print(f"Lỗi kết nối database: {e}")
            raise

    def disconnect(self):
        """Đóng kết nối database"""
        if self.connection:
            self.cursor.close()
            self.connection.close()
            self.connection = None
            self.cursor = None
            print("Đã đóng kết nối database!")

    def execute_query(self, query, params=None):
        """Thực thi câu truy vấn SQL"""
        try:
            self.connect()
            self.cursor.execute(query, params or ())
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"Lỗi thực thi truy vấn: {e}")
            raise
        finally:
            self.disconnect()

    def fetch_all(self, query, params=None):
        """Lấy tất cả kết quả từ câu truy vấn SELECT"""
        try:
            self.connect()
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Lỗi truy vấn dữ liệu: {e}")
            raise
        finally:
            self.disconnect()

    def fetch_one(self, query, params=None):
        """Lấy một kết quả từ câu truy vấn SELECT"""
        try:
            self.connect()
            self.cursor.execute(query, params or ())
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Lỗi truy vấn dữ liệu: {e}")
            raise
        finally:
            self.disconnect()


# Module-level instance for easy imports from other modules
# Usage: from app.database import db
db = Database()

