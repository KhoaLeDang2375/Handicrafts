import React, { useEffect, useState } from 'react';
import { getBlogs } from '../../services/blogApi';
import './BlogPage.scss'; 

const BlogPage = () => {
  const [blogs, setBlogs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadBlogs();
  }, []);

  const loadBlogs = async () => {
    try {
      const data = await getBlogs();
      setBlogs(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="blog-container">Đang tải bài viết...</div>;

  return (
    <div className="blog-container">
      <div className="blog-header">
        <h1>Góc Chia Sẻ & Tin Tức</h1>
        <p>Những câu chuyện thú vị từ Aura Craft</p>
      </div>

      <div className="blog-grid">
        {blogs.length > 0 ? (
          blogs.map((blog) => (
            <div key={blog.id} className="blog-card">
              {/* Giả sử backend trả về field 'created_at' hoặc 'id' */}
              <div className="blog-content">
                <p>{blog.content}</p>
              </div>
              <div className="blog-footer">
                <span>Tác giả ID: {blog.Author_id}</span>
                {/* Bạn có thể format ngày tháng ở đây */}
              </div>
            </div>
          ))
        ) : (
          <p>Chưa có bài viết nào.</p>
        )}
      </div>
    </div>
  );
};

export default BlogPage;