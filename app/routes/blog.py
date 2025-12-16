from fastapi import APIRouter, HTTPException, Path, Query
from app.schemas import *
from app.models.blog import Blog
from app.security import verify_access_token
from jose import JWTError
from fastapi import File, UploadFile, Form
import shutil
import os
import uuid

# Định nghĩa thư mục lưu
UPLOAD_DIR = "app/static/images"

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
    author_id: int = Path(..., description="Author id to filter blogs"),
    skip: int = Query(0, ge=0, description="Number of blogs to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of blogs to return")
):
    """Retrieve blog posts by a specific author"""
    try:
        blogs = Blog.get_by_author(author_id, skip=skip, limit=limit)
        return blogs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/blogs/", response_model=BlogResponse)
async def create_blog(
    # blog: BlogBase,
    title: str = Form(...),       
    content: str = Form(...),     
    image: UploadFile = File(None),
    access_token: str = Query(..., description="Access token of the employee creating the blog")
):
    """Create a new blog post"""
    try:
        payload = verify_access_token(access_token)
        if payload['role'] != 'employee':
            raise HTTPException(status_code=403, detail="Only employees can create blogs")
        author_id = int(payload['sub'])
        author_name = payload.get('name')

        image_url_db = None
        # Xử lý lưu ảnh nếu có
        if image:
            # 1. TẠO TÊN FILE DUY NHẤT (UUID)
            # Lấy đuôi file (ví dụ: .png, .jpg)
            file_extension = image.filename.split(".")[-1]
            # Tạo tên mới: uuid + đuôi file
            unique_filename = f"{uuid.uuid4()}.{file_extension}"
            
            # 2. LƯU FILE VÀO Ổ CỨNG
            # Đường dẫn vật lý: app/static/images/uuid.png
            file_location = os.path.join(UPLOAD_DIR, unique_filename)
            
            with open(file_location, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
            
            # 3. TẠO ĐƯỜNG DẪN ĐỂ LƯU VÀO DATABASE
            # Đây là chuỗi bạn sẽ lưu vào cột image_url
            # Frontend sẽ gọi: http://localhost:8000/static/images/uuid.png
            image_url_db = f"/static/images/{unique_filename}"

        # Lưu vào DB
        new_blog = Blog(
            author_id=author_id, 
            title=title, 
            content=content,
            author_name=author_name,
            image_url=image_url_db
        )

        blog_id = new_blog.save()
        created_blog = Blog.get_by_id(blog_id)
        return created_blog
    
    except Exception as e:
        print(f"Lỗi tạo blog: {e}") 
        raise HTTPException(status_code=500, detail=str(e))
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid access token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/blogs/{blog_id}", response_model=BlogResponse)
async def update_blog(
    blog_id: int = Path(..., description="Blog id to update"),
    # blog: BlogBase = ...,
    title: str = Form(...),       
    content: str = Form(...),     
    image: UploadFile = File(None),
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
        
        # 3. Xử lý ảnh, mặc định lấy ảnh cũ
        final_image_url = existing_blog.get('image_url')

        # Nếu người dùng có upload ảnh mới
        if image:
            # -- Logic lưu file (giống hàm create) --
            UPLOAD_DIR = "app/static/images"
            file_extension = image.filename.split(".")[-1]
            unique_filename = f"{uuid.uuid4()}.{file_extension}"
            file_location = os.path.join(UPLOAD_DIR, unique_filename)
            
            with open(file_location, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
            
            # Cập nhật đường dẫn mới
            final_image_url = f"/static/images/{unique_filename}"
            
            # 4. Gọi Model để update
        Blog.update_content(blog_id, title, content, final_image_url)
        
        return Blog.get_by_id(blog_id)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid access token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# Delete blog post
@router.delete("/blogs/{blog_id}")
async def delete_blog(
    blog_id: int = Path(..., description="Blog id to delete"),
    access_token: str = Query(..., description="Access token of the employee deleting the blog")
):
    """Delete a blog post"""
    try:
        payload = verify_access_token(access_token)
        if payload['role'] != 'employee':
            raise HTTPException(status_code=403, detail="Only employees can delete blogs")
        existing_blog = Blog.get_by_id(blog_id)
        if not existing_blog:
            raise HTTPException(status_code=404, detail="Blog not found")
        Blog.delete(blog_id)
        return {"detail": "Blog deleted successfully"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid access token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))