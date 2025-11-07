from app.routes.products import router as products_router
from app.routes.reviews import router as reviews_router
from app.routes.signup import router as signup_router
from app.routes.login import router as login_router
__all__ = ['products_router', 'reviews_router','signup_router','login_router']