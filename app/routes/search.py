from fastapi import APIRouter, HTTPException, Query, Request
from typing import List, Optional
from app.schemas import SearchResult
from app.search_service.search import VectorSearch


router = APIRouter(
    prefix="/search",
    tags=["searchproduct"]
)


@router.get('/', response_model=List[SearchResult])
async def searchproduct(request: Request, q: str = Query(..., min_length=1, description="Search query"), k: int = Query(5, ge=1, le=50)):
    """Search products using vector search stored in Redis.

    q: query text
    k: number of nearest neighbors to return
    """
    try:
        # reuse singleton created at app startup if available
        vs = getattr(request.app.state, "vector_search", None)
        if vs is None:
            # fallback to creating a local one (loads model)
            vs = VectorSearch()
        results = vs.search(q, k=k)
        # results already in dict form matching SearchResult fields
        return results
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {e}")
