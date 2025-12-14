import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom'; 
import { getBlogs } from '../../services/blogApi';
import { FiUser, FiCalendar } from 'react-icons/fi';
import './BlogPage.scss';

import bannerImg from '../../assets/images/blogs.jpg';

const BlogPage = () => {
  const [blogs, setBlogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate(); // Hook điều hướng

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

  console.log("Kết quả Blog", blogs);
  // Hàm xử lý khi click vào box
  const handleCardClick = (id) => {
    navigate(`/blog/${id}`);
  };

  if (loading) return <div className="blog-container">Đang tải...</div>;

  return (
    <div className="blog-page-wrapper">
      
      <div 
        className="blog-banner"
        style={{ backgroundImage: `url(${bannerImg})` }} 
      >
        <div className="banner-content">
          <h1>Góc Chia Sẻ</h1>
          <p>Kiến thức và câu chuyện từ Aura Craft</p>
        </div>
      </div>

      {/* --- PHẦN NỘI DUNG CHÍNH --- */}
      <div className="blog-container">
        <div className="blog-grid">
          {blogs.map((blog) => (
            <div 
              key={blog.id} 
              className="blog-card clickable" 
              onClick={() => handleCardClick(blog.id)}
              style={{ cursor: 'pointer' }}
            >
              <div className="blog-content">
                <h3 className="blog-title">{blog.title || "Không có tiêu đề"}</h3>
                
                <div className="blog-meta">
                  <span><FiUser /> {blog.author_name}</span>
                  <span><FiCalendar /> {blog.create_time ? new Date(blog.create_time).toLocaleDateString('vi-VN') : ''}</span>
                </div>

                <p className="blog-desc">
                  {blog.content}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default BlogPage;