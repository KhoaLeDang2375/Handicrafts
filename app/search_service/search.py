from sentence_transformers import SentenceTransformer
import numpy as np
from redis.commands.search.field import TextField, VectorField
from redis.commands.search.index_definition import IndexDefinition, IndexType
from app.database.redis_client import redis_client, RedisClient
from redis import exceptions as redis_exceptions
from redis.commands.search.query import Query


class VectorSearch:
    def __init__(self, redis: RedisClient = redis_client, index_name="product_idx", prefix="product:", dim=384):
        self.redis = redis
        self.index_name = index_name
        self.prefix = prefix
        self.dim = dim
        # load model once per instance
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self._ensure_index()

    def _ensure_index(self):
        try:
            self.redis.connect().ft(self.index_name).create_index([
                TextField("name"),
                TextField("description"),
                VectorField("embedding", "HNSW", {"TYPE": "FLOAT32", "DIM": self.dim, "DISTANCE_METRIC": "COSINE"})
            ],
            definition=IndexDefinition(prefix=[self.prefix], index_type=IndexType.HASH))
            print(f"Created index {self.index_name}")
        except Exception:
            # index may already exist or server doesn't support FT.CREATE
            pass

    def get_embedding(self, text: str):
        return np.array(self.model.encode(text), dtype=np.float32)

    def add_product(self, product_id: int):
        """Fetch product from MySQL and store a minimal hash in Redis including embedding."""
        from app.models.product import Product
        product = Product.get_by_id(product_id)
        if not product:
            raise ValueError(f"Product id {product_id} not found in DB")

        name = product.get("name")
        description = product.get("description") or ""
        category_id = product.get("product_category_id") or product.get("category_id")
        category_name = product.get("category_name")
        status = product.get("status")

        emb = self.get_embedding(f"{name} {description}")
        mapping = {
            "product_id": str(product_id),
            "name": name,
            "description": description,
            "embedding": emb.tobytes(),
            "category_id": str(category_id) if category_id else "",
            "category_name": category_name or "",
            "status": str(status) if status else ""
        }
        # store as hash
        self.redis.connect().hset(f"{self.prefix}{product_id}", mapping=mapping)

    def add_product_from_record(self, product_record: dict):
        """Add product to redis using a product record (dict) to avoid extra DB roundtrips.

        product_record should contain at least: id, name, description, category_name, status
        """
        product_id = product_record.get("id")
        if not product_id:
            raise ValueError("product_record must contain 'id'")
        name = product_record.get("name")
        description = product_record.get("description") or ""
        category_id = product_record.get("product_category_id") or product_record.get("category_id")
        category_name = product_record.get("category_name")
        status = product_record.get("status")

        emb = self.get_embedding(f"{name} {description}")
        mapping = {
            "product_id": str(product_id),
            "name": name,
            "description": description,
            "embedding": emb.tobytes(),
            "category_id": str(category_id) if category_id else "",
            "category_name": category_name or "",
            "status": str(status) if status else ""
        }
        self.redis.connect().hset(f"{self.prefix}{product_id}", mapping=mapping)

    def search(self, query: str, k=5):
        """Search using RediSearch FT.SEARCH when available, otherwise fallback to local scan+numpy KNN.

        Returns list of dicts: {product_id, name, description, category_name, score}
        """
        query_emb = self.get_embedding(query).astype(np.float32).tobytes()
        q = f"*=>[KNN {k} @embedding $vec as score]"
        params_dict = {"vec": query_emb}

        try:
            # Try RediSearch vector KNN
            # Use the Query builder to set sort_by / return fields / dialect —
            # redis-py search() does not accept `sort_by` as a direct kwarg.
            query = Query(q).sort_by("score").return_fields("product_id", "name", "description", "category_name", "score").dialect(2)
            results = self.redis.connect().ft(self.index_name).search(query, query_params=params_dict)
            out = []
            for doc in results.docs:
                prod_id = getattr(doc, "product_id", None) or getattr(doc, "id", "").split(":")[-1]
                out.append({
                    "product_id": int(prod_id) if prod_id and str(prod_id).isdigit() else prod_id,
                    "name": getattr(doc, "name", ""),
                    "description": getattr(doc, "description", ""),
                    "category_name": getattr(doc, "category_name", ""),
                    "score": float(getattr(doc, "score", 0.0))
                })
            return out
        except redis_exceptions.ResponseError as e:
            msg = str(e)
            if "FT.SEARCH" in msg or "unknown command" in msg:
                # RediSearch not available on Redis server -> fallback
                print("[VectorSearch] RediSearch not available, falling back to local scan (slow for large datasets)")
                return self._fallback_search(query_emb, k)
            raise

    def _fallback_search(self, query_emb_bytes: bytes, k: int):
        r = self.redis.connect()
        query_vec = np.frombuffer(query_emb_bytes, dtype=np.float32)
        items = []  # (sim, product_id, name, description, category_name)

        # iterate all keys with prefix; note: slow for large datasets
        for key in r.scan_iter(match=f"{self.prefix}*"):
            try:
                h = r.hgetall(key)
                emb_b = h.get("embedding")
                if not emb_b:
                    continue
                emb = np.frombuffer(emb_b, dtype=np.float32)
                denom = (np.linalg.norm(query_vec) * np.linalg.norm(emb))
                if denom == 0:
                    sim = 0.0
                else:
                    sim = float(np.dot(query_vec, emb) / denom)
                product_id = h.get("product_id") or key.split(":")[-1]
                items.append((sim, product_id, h.get("name", ""), h.get("description", ""), h.get("category_name", "")))
            except Exception:
                continue

        items.sort(key=lambda x: x[0], reverse=True)
        out = []
        for sim, pid, name, desc, cat in items[:k]:
            out.append({
                "product_id": int(pid) if pid and str(pid).isdigit() else pid,
                "name": name,
                "description": desc,
                "category_name": cat,
                "score": sim,
            })
        return out


# Hàm đồng bộ toàn bộ sản phẩm từ MySQL lên Redis
def sync_all_products_to_redis(vs: VectorSearch | None = None):
    """Synchronize all products from MySQL into Redis.

    If `vs` (VectorSearch instance) is provided, it will be reused. Otherwise a temporary
    VectorSearch will be created (which loads the embedding model).
    """
    from app.models.product import Product
    own_vs = False
    if vs is None:
        vs = VectorSearch()
        own_vs = True

    products = Product.get_all(skip=0, limit=10000)  # lấy tối đa 10k sản phẩm, tuỳ chỉnh nếu cần
    for p in products:
        try:
            # use the record directly to avoid extra DB fetch per product
            vs.add_product_from_record(p)
        except Exception as e:
            print(f"[Redis sync] Lỗi với sản phẩm id={p['id']}: {e}")
    print(f"[Redis sync] Đã đồng bộ {len(products)} sản phẩm lên Redis.")

    # if we created a temporary VectorSearch, close its redis connection to avoid leaks
    if own_vs:
        try:
            vs.redis.close()
        except Exception:
            pass
