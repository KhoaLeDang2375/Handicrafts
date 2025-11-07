from fastapi import APIRouter, HTTPException, Path, Query
from app.schemas import *
from app.models.blog import Blog
from app.security import verify_access_token
from jose import JWTError
router = APIRouter(
    tags=["blogs"]
)

@router.get("/blogs/{blog_id}", response_model=BlogResponse)
async def get_blog_by_id(
    blog_id: int = Path(..., description="Blog id to retrieve")
):
    """Retrieve a blog post by its ID"""
    try:
        blog = Blog.get_by_id(blog_id)
        if not blog:
            raise HTTPException(status_code=404, detail="Blog not found")
        return blog
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@router.get("/blogs/", response_model=list[BlogResponse])
async def get_blogs(
    skip: int = Query(0, ge=0, description="Number of blogs to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of blogs to return")
):
    """Retrieve a list of blog posts with pagination"""
    try:
        blogs = Blog.get_all(skip=skip, limit=limit)
        return blogs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@router.get("/blogs/author/{author_id}", response_model=list[BlogResponse])
async def get_blogs_by_author(
    author_id: int = Path(..., description="Author id to filter blogs")
):
    """Retrieve blog posts by a specific author"""
    try:
        blogs = Blog.get_by_author(author_id)
        return blogs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@router.post("/blogs/", response_model=BlogResponse)
async def create_blog(
    blog: BlogBase,
    access_token: str = Query(..., description="Access token of the employee creating the blog")
):
    """Create a new blog post"""
    try:
        payload = verify_access_token(access_token)
        if payload['role'] != 'employee':
            raise HTTPException(status_code=403, detail="Only employees can create blogs")
        author_id = payload['user_id']
        new_blog = Blog(author_id=author_id, content=blog.content)
        blog_id = new_blog.save()
        created_blog = Blog.get_by_id(blog_id)
        return created_blog
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid access token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@router.put("/blogs/{blog_id}", response_model=BlogResponse)
async def update_blog(
    blog_id: int = Path(..., description="Blog id to update"),
    blog: BlogBase = ...,
    access_token: str = Query(..., description="Access token of the employee updating the blog")
):
    """Update an existing blog post"""
    try:
        payload = verify_access_token(access_token)
        if payload['role'] != 'employee':
            raise HTTPException(status_code=403, detail="Only employees can update blogs")
        existing_blog = Blog.get_by_id(blog_id)
        if not existing_blog:
            raise HTTPException(status_code=404, detail="Blog not found")
        blog_model = Blog(author_id=existing_blog['Author_id'], content=blog.content)
        blog_model.update_content(blog_id, blog.content)
        updated_blog = Blog.get_by_id(blog_id)
        return updated_blog
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid access token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
