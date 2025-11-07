from fastapi import APIRouter, HTTPException, Path, Query
from app.schemas import *
from app.models.review import Review
from app.models.product import Product
from app.models.product_variant import ProductVariant
from app.security import verify_access_token
from jose import JWTError
router = APIRouter(
    tags=["reviews"]
)



@router.post("/variants/{variant_id}/reviews", response_model=ReviewResponse)
async def create_review_for_variant(
    variant_id: int = Path(..., description="Variant id to review"),
    review: ReviewCreate = None
):
    """Create a review for a specific product variant"""
    try:
        payload = verify_access_token(review.access_token)
        # Lấy thông tin customer và chuyển về số
        customer_id = int(payload.get("sub"))
        # Ensure variant exists
        variant = ProductVariant.get_by_id(variant_id)
        if not variant:
            raise HTTPException(status_code=404, detail="Variant not found")
            
        # Check if user has bought the item
        if not Review.check_user_buy_item(customer_id, variant_id):
            raise HTTPException(
                status_code=403,
                detail="You can only review items you have purchased and received"
            )
        new_review = Review(
            customer_id=customer_id,
            variant_id=variant_id,
            rating=review.rating,
            content=review.content
        )
        success = new_review.save()
        if not success:
            raise HTTPException(status_code=500, detail="Failed to save review")

        # Fetch the most recent review for this variant
        reviews = Review.get_by_product_variant(variant_id)
        created = reviews[0] if reviews else None
        if not created:
            raise HTTPException(status_code=500, detail="Review created but cannot be retrieved")

        return created
    except JWTError as e:
        raise HTTPException(
            status_code=401,
            detail=f"Could not validate credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/variants/{variant_id}/reviews", response_model=PaginatedReviewList)
async def list_reviews_for_variant(
    variant_id: int = Path(..., description="Variant id"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """List reviews for a variant (paginated)"""
    try:
        variant = ProductVariant.get_by_id(variant_id)
        if not variant:
            raise HTTPException(status_code=404, detail="Variant not found")

        reviews = Review.get_by_product_variant(variant_id)
        total = Review.count_by_variant(variant_id)

        # Apply pagination in-memory (the model already supports LIMIT but we keep safety)
        sliced = reviews[skip: skip + limit]

        return {"items": sliced, "total": total, "skip": skip, "limit": limit}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/products/{product_id}/reviews", response_model=PaginatedReviewList)
async def list_reviews_for_product(
    product_id: int = Path(..., description="Product id"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=200)
):
    """List reviews for all variants of a product (aggregated)"""
    try:
        product = Product.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        variants = ProductVariant.get_by_product(product_id) or []
        all_reviews = []
        for v in variants:
            rv = Review.get_by_product_variant(v['id']) or []
            all_reviews.extend(rv)

        # sort reviews by date desc if date exists
        try:
            all_reviews.sort(key=lambda x: x.get('date', ''), reverse=True)
        except Exception:
            pass

        total = len(all_reviews)
        sliced = all_reviews[skip: skip + limit]
        return {"items": sliced, "total": total, "skip": skip, "limit": limit}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/reviews/{review_id}", response_model=ReviewResponse)
async def get_review(review_id: int = Path(..., description="Review id")):
    """Get a single review by id"""
    try:
        r = Review.get_by_id(review_id)
        if not r:
            raise HTTPException(status_code=404, detail="Review not found")
        return r
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/reviews/{review_id}", response_model=ReviewResponse)
async def update_review(review_id: int = Path(..., description="Review id"), data: ReviewUpdate = None):
    """Update rating or content of a review"""
    try:
        # Xác thực token
        payload = verify_access_token(data.access_token)
        customer_id = int(payload.get("sub"))

        # Kiểm tra review tồn tại
        existing = Review.get_by_id(review_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Review not found")

        # Kiểm tra quyền sở hữu review
        if existing.get('customer_id') != customer_id:
            raise HTTPException(
                status_code=403,
                detail="You can only update your own reviews"
            )

        # Cập nhật review
        success = Review.update(review_id, rating=data.rating, content=data.content)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update review")

        updated = Review.get_by_id(review_id)
        return updated
    except JWTError as e:
        raise HTTPException(
            status_code=401,
            detail=f"Could not validate credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/reviews/{review_id}")
async def delete_review(
    review_id: int = Path(..., description="Review id"),
    data: ReviewDelete = None
):
    """Delete a review"""
    try:
        # Xác thực token
        payload = verify_access_token(data.access_token)
        customer_id = int(payload.get("sub"))

        # Kiểm tra review tồn tại
        existing = Review.get_by_id(review_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Review not found")

        # Kiểm tra quyền sở hữu review
        if existing.get('customer_id') != customer_id:
            raise HTTPException(
                status_code=403,
                detail="You can only delete your own reviews"
            )

        # Xóa review
        success = Review.delete(review_id)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete review")

        return {"message": "Review deleted"}
    except JWTError as e:
        raise HTTPException(
            status_code=401,
            detail=f"Could not validate credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
