
import os
import redis

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

class RedisClient:
    def __init__(self, url=REDIS_URL):
        self.url = url
        self.client = None

    def connect(self):
        if not self.client:
            # Use raw bytes responses so binary embeddings are preserved when stored/retrieved
            self.client = redis.from_url(self.url, decode_responses=False)
        return self.client

    def close(self):
        if self.client:
            try:
                self.client.close()
            except Exception:
                pass
            self.client = None

    def set(self, key, value, ex=None):
        self.connect()
        return self.client.set(key, value, ex=ex)

    def get(self, key):
        self.connect()
        return self.client.get(key)

    def delete(self, key):
        self.connect()
        return self.client.delete(key)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

# Singleton instance
redis_client = RedisClient()

def get_redis_client():
    """Lấy instance RedisClient (singleton)"""
    return redis_client