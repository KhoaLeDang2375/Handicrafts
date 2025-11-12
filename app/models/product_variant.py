from app.database import db
import html
import bleach

class ProductVariant:
    MAX_COLOR_LEN = 100
    MAX_SIZE_LEN = 50

    def __init__(self, product_id, color, size, price, amount):
        self.product_id = int(product_id)
        self.color = self._sanitize_text(color, self.MAX_COLOR_LEN)
        self.size = self._sanitize_text(size, self.MAX_SIZE_LEN)
        self.price = float(price)
        self.amount = int(amount)

    # ----------------------------
    #    Helper làm sạch dữ liệu
    # ----------------------------
    @staticmethod
    def _sanitize_text(text, max_len):
        text = text.strip() if text else ""
        text = bleach.clean(html.escape(text), tags=[], attributes={}, strip=True)
        return text[:max_len]

    # ----------------------------
    #    CREATE
    # ----------------------------
    def save(self):
        query = """
        INSERT INTO ProductVariant (product_id, color, size, price, amount)
        VALUES (%s, %s, %s, %s, %s)
        """
        return db.execute_query(query, (
            self.product_id,
            self.color,
            self.size,
            self.price,
            self.amount
        ))

    # ----------------------------
    #   READ
    # ----------------------------
    @staticmethod
    def get_by_id(variant_id):
        query = """
        SELECT v.*, p.name AS product_name 
        FROM ProductVariant v
        JOIN Products p ON v.product_id = p.id
        WHERE v.id = %s
        """
        return db.fetch_one(query, (variant_id,))

    @staticmethod
    def get_by_product(product_id, variant_id=None, get_one=False):
        if get_one and variant_id is not None:
            query = """
            SELECT * FROM ProductVariant
            WHERE product_id = %s AND id = %s
            LIMIT 1
            """
            return db.fetch_one(query, (product_id, variant_id))
        else:
            query = """
            SELECT * FROM ProductVariant
            WHERE product_id = %s
            ORDER BY id ASC
            """
            return db.fetch_all(query, (product_id,))

    # ----------------------------
    #    UPDATE (tổng quát)
    # ----------------------------
    @staticmethod
    def update(variant_id, color=None, size=None, price=None, amount=None):
        """Cập nhật linh hoạt thông tin biến thể."""
        fields = []
        values = []

        if color is not None:
            fields.append("color = %s")
            values.append(ProductVariant._sanitize_text(color, ProductVariant.MAX_COLOR_LEN))
        if size is not None:
            fields.append("size = %s")
            values.append(ProductVariant._sanitize_text(size, ProductVariant.MAX_SIZE_LEN))
        if price is not None:
            try:
                values.append(float(price))
                fields.append("price = %s")
            except ValueError:
                raise ValueError("Giá sản phẩm không hợp lệ.")
        if amount is not None:
            try:
                values.append(int(amount))
                fields.append("amount = %s")
            except ValueError:
                raise ValueError("Số lượng phải là số nguyên.")

        if not fields:
            return None  # Không có gì để cập nhật

        set_clause = ", ".join(fields)
        query = f"UPDATE ProductVariant SET {set_clause} WHERE id = %s"
        values.append(variant_id)

        return db.execute_query(query, tuple(values))

    # ----------------------------
    #    UPDATE STOCK (riêng biệt, có giới hạn)
    # ----------------------------
    @staticmethod
    def update_stock(variant_id, delta_amount):
        """Tăng hoặc giảm số lượng tồn kho một cách an toàn."""
        try:
            delta = int(delta_amount)
        except ValueError:
            raise ValueError("Số lượng thay đổi không hợp lệ.")

        query = """
        UPDATE ProductVariant
        SET amount = GREATEST(amount + %s, 0)  -- tránh âm kho
        WHERE id = %s
        """
        return db.execute_query(query, (delta, variant_id))

    # ----------------------------
    #    DELETE
    # ----------------------------
    @staticmethod
    def delete(variant_id):
        query = "DELETE FROM ProductVariant WHERE id = %s"
        return db.execute_query(query, (variant_id,))
