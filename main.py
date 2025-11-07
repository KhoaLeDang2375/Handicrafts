from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import products_router, signup_router,login_router, search_router
# Import search service
from app.search_service.search import sync_all_products_to_redis, VectorSearch
from app.database.redis_client import redis_client

app = FastAPI(
    title="Handicraft API",
    description="API for handicraft e-commerce website",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to Handicraft API"}

# Include routers
app.include_router(products_router)
# Search router
app.include_router(search_router)
# app.include_router(reviews_router)


@app.on_event("startup")
def startup_event():
    """Create a singleton VectorSearch at startup and sync Redis."""
    try:
        vs = VectorSearch()
        app.state.vector_search = vs
        # sync products into redis using the created instance
        try:
            sync_all_products_to_redis(vs)
        except Exception as e:
            print(f"[startup] sync_all_products_to_redis failed: {e}")
    except Exception as e:
        print(f"[startup] Failed to initialize VectorSearch: {e}")


@app.on_event("shutdown")
def shutdown_event():
    # try to close redis connections gracefully
    try:
        if hasattr(app.state, "vector_search"):
            app.state.vector_search.redis.close()
    except Exception:
        pass
app.include_router(signup_router)
app.include_router(login_router)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)