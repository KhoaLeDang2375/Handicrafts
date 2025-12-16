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
        self.in_transaction = False

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

    def begin_transaction(self):
        """Bắt đầu một transaction. Kết nối được giữ mở cho đến khi commit/rollback."""
        try:
            if not self.connection:
                self.connect()
            self.in_transaction = True
        except Exception as e:
            print(f"Lỗi khi bắt đầu transaction: {e}")
            raise

    def commit_transaction(self):
        """Commit current transaction and disconnect."""
        try:
            if self.connection:
                self.connection.commit()
        finally:
            # End transaction and disconnect
            self.in_transaction = False
            self.disconnect()

    def rollback_transaction(self):
        """Rollback current transaction and disconnect."""
        try:
            if self.connection:
                self.connection.rollback()
        finally:
            self.in_transaction = False
            self.disconnect()

    def execute_query(self, query, params=None):
        """Thực thi câu truy vấn SQL"""
        try:
            self.connect()
            self.cursor.execute(query, params or ())
            # If we're not inside an explicit transaction, commit and disconnect here
            if not self.in_transaction:
                self.connection.commit()
                # capture lastrowid before disconnecting
                lastrowid = self.cursor.lastrowid
                self.disconnect()
                return lastrowid if lastrowid else True
            else:
                # inside transaction: return lastrowid or True but keep connection open
                lastrowid = self.cursor.lastrowid
                return lastrowid if lastrowid else True
        except Exception as e:
            # If connection exists and we're in transaction, rollback will be handled by caller
            try:
                if self.connection:
                    self.connection.rollback()
            except Exception:
                pass
            print(f"Lỗi thực thi truy vấn: {e}")
            raise
        finally:
            # Only disconnect when not in transaction. If in transaction, caller manages disconnect.
            if not self.in_transaction and self.connection:
                # disconnect already handled above for success branch, but ensure cleanup on failures
                try:
                    self.disconnect()
                except Exception:
                    pass

    def fetch_all(self, query, params=None):
        """Lấy tất cả kết quả từ câu truy vấn SELECT"""
        try:
            self.connect()
            self.cursor.execute(query, params or ())
            results = self.cursor.fetchall()
            return results
        except Exception as e:
            print(f"Lỗi truy vấn dữ liệu: {e}")
            raise
        finally:
            if not self.in_transaction:
                self.disconnect()

    def fetch_one(self, query, params=None):
        """Lấy một kết quả từ câu truy vấn SELECT"""
        try:
            self.connect()
            self.cursor.execute(query, params or ())
            result = self.cursor.fetchone()
            return result
        except Exception as e:
            print(f"Lỗi truy vấn dữ liệu: {e}")
            raise
        finally:
            if not self.in_transaction:
                self.disconnect()


# Module-level instance for easy imports from other modules
# Usage: from app.database import db
db = Database()

