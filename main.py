from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import products_router, signup_router,login_router,reviews_router, blogs_router

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
app.include_router(reviews_router)
app.include_router(signup_router)
app.include_router(login_router)
app.include_router(blogs_router)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)