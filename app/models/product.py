from app.database import db
from datetime import datetime
import html
import bleach

class Product:
    MAX_NAME_LEN = 255
    MAX_DESC_LEN = 2000
    MAX_ARTISAN_DESC_LEN = 2000
    MAX_LIMIT = 100  # tránh client gửi limit quá lớn gây DoS

    def __init__(self, name, description, category_id, status, artisan_description, image_url=None):
        # --- Làm sạch & kiểm soát dữ liệu đầu vào ---
        self.name = self._sanitize_text(name, self.MAX_NAME_LEN)
        self.description = self._sanitize_html(description, self.MAX_DESC_LEN)
        self.category_id = int(category_id)
        self.status = int(status)
        self.artisan_description = self._sanitize_html(artisan_description, self.MAX_ARTISAN_DESC_LEN)
        self.image_url = image_url

    # --- Hàm làm sạch dữ liệu ---
    @staticmethod
    def _sanitize_text(text: str, max_len: int) -> str:
        """Loại bỏ ký tự thừa và escape HTML hoàn toàn (chỉ text thuần)."""
        text = text.strip() if text else ""
        text = html.escape(text)  # loại bỏ <script>...
        return text[:max_len]

    @staticmethod
    def _sanitize_html(text: str, max_len: int) -> str:
        """Cho phép một số tag cơ bản, loại bỏ script và thuộc tính nguy hiểm."""
        allowed_tags = ['b', 'i', 'u', 'em', 'strong', 'br', 'p']
        cleaned = bleach.clean(text or "", tags=allowed_tags, attributes={}, strip=True)
        return cleaned[:max_len]

    # --- Lưu vào DB ---
    def save(self):
        query = """
        INSERT INTO Products (name, description, category_id, status, artisan_description, image_url)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        return db.execute_query(query, (
            self.name,
            self.description,
            self.category_id,
            self.status,
            self.artisan_description,
            self.image_url
        ))

    # --- Lấy danh sách sản phẩm ---
    @staticmethod
    def get_all(skip=0, limit=10):
        limit = min(max(0, limit), Product.MAX_LIMIT)
        skip = max(0, skip)

        query = """
        SELECT 
            p.id,
            p.name,
            p.description,
            p.category_id,
            p.status,
            p.artisan_description,
            p.image_url,
            c.name AS category_name,
            c.id AS category_id
        FROM Products p
        LEFT JOIN Categories c ON p.category_id = c.id
        ORDER BY p.id
        LIMIT %s OFFSET %s
        """
        return db.fetch_all(query, (limit, skip))

    # --- Đếm tất cả sản phẩm ---
    @staticmethod
    def count_all():
        query = "SELECT COUNT(*) AS total FROM Products"
        result = db.fetch_one(query)
        return result['total'] if result else 0

    # --- Lấy sản phẩm theo ID ---
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
            p.image_url,
            c.name AS category_name,
            c.id AS category_id,
            JSON_OBJECT(
                'id', c.id,
                'name', c.name
            ) AS category
        FROM Products p
        LEFT JOIN Categories c ON p.category_id = c.id
        WHERE p.id = %s
        """
        return db.fetch_one(query, (product_id,))

    # --- Lấy theo category ---
    @staticmethod
    def get_by_category(category_id, skip=0, limit=10):
        limit = min(max(0, limit), Product.MAX_LIMIT)
        skip = max(0, skip)

        query = """
        SELECT 
            p.id,
            p.name,
            p.description,
            p.category_id,
            p.status,
            p.artisan_description,
            p.image_url,
            c.name AS category_name,
            c.id AS category_id
        FROM Products p
        LEFT JOIN Categories c ON p.category_id = c.id
        WHERE p.category_id = %s
        ORDER BY p.id
        LIMIT %s OFFSET %s
        """
        return db.fetch_all(query, (category_id, limit, skip))

    # --- Đếm theo category ---
    @staticmethod
    def count_by_category(category_id):
        query = "SELECT COUNT(*) AS total FROM Products WHERE category_id = %s"
        result = db.fetch_one(query, (category_id,))
        return result['total'] if result else 0
    @staticmethod
    def update(product_id, name=None, description=None, category_id=None, status=None, artisan_description=None):
        """Cập nhật thông tin sản phẩm theo ID (chỉ cập nhật field có giá trị)."""
        fields = []
        values = []

        # Xử lý & làm sạch dữ liệu trước khi lưu
        if name is not None:
            fields.append("name = %s")
            values.append(Product._sanitize_text(name, Product.MAX_NAME_LEN))
        if description is not None:
            fields.append("description = %s")
            values.append(Product._sanitize_html(description, Product.MAX_DESC_LEN))
        if category_id is not None:
            fields.append("category_id = %s")
            values.append(int(category_id))
        if status is not None:
            fields.append("status = %s")
            values.append(int(status))
        if artisan_description is not None:
            fields.append("artisan_description = %s")
            values.append(Product._sanitize_html(artisan_description, Product.MAX_ARTISAN_DESC_LEN))

        if not fields:
            return None  # Không có gì để cập nhật

        set_clause = ", ".join(fields)
        query = f"UPDATE Products SET {set_clause} WHERE id = %s"
        values.append(product_id)

        return db.execute_query(query, tuple(values))

    @staticmethod
    def delete(product_id):
        """Xóa sản phẩm theo ID."""
        query = "DELETE FROM Products WHERE id = %s"
        return db.execute_query(query, (product_id,))