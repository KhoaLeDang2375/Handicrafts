"""Resync all products into Redis embeddings.

Usage:
    # run with project's venv python
    ./venv/bin/python scripts/resync_redis.py

This will:
- create a VectorSearch instance (loads the embedding model once)
- call sync_all_products_to_redis(vs) to overwrite stored embeddings in Redis
- close the Redis connection when finished

Be careful: this loads the sentence-transformers model and may use memory/CPU.
"""

from app.search_service.search import VectorSearch, sync_all_products_to_redis


def main():
    print("Starting full redis resync of products...")
    vs = None
    try:
        vs = VectorSearch()
        sync_all_products_to_redis(vs)
        print("Resync completed.")
    except Exception as e:
        print(f"Resync failed: {e}")
    finally:
        try:
            if vs is not None:
                vs.redis.close()
        except Exception:
            pass


if __name__ == '__main__':
    main()
