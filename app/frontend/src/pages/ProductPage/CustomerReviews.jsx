import { useState, useEffect } from 'react';
import './CustomerReviews.scss';

// Link API giả lập
const API_URL = 'http://localhost:8000/reviews';

const CustomerReviews = () => {
  const [reviews, setReviews] = useState([]);
  const [isExpanded, setIsExpanded] = useState(false); 

  // Lấy dữ liệu từ API
  useEffect(() => {
    const fetchReviews = async () => {
      try {
        const res = await fetch(API_URL);
        const data = await res.json();
        
        // Kiểm tra an toàn: chỉ set nếu data là mảng
        if (Array.isArray(data)) {
            setReviews(data);
        } else {
            setReviews([]); 
        }
      } catch (err) {
        console.error("Lỗi tải đánh giá:", err);
        setReviews([]);
      }
    };

    fetchReviews();
  }, []);

  // Logic cắt mảng
  const visibleReviews = isExpanded ? reviews : reviews.slice(0, 3);

  const toggleExpand = () => {
    setIsExpanded(!isExpanded);
  };

  // Hàm render sao đánh giá (Vd: rating = 5 -> ★★★★★)
  const renderStars = (rating) => {
    return "★".repeat(rating || 5); // Mặc định 5 sao nếu thiếu data
  };

  return (
    <section className="customer-reviews">
      <div className="reviews-container">
        
        {/* Header */}
        <div className="reviews-header">
          <h2 className="title">Đánh giá từ khách hàng</h2>
          
          {/* Chỉ hiện nút xem thêm nếu có nhiều hơn 3 đánh giá */}
          {reviews.length > 3 && (
            <button className="toggle-btn" onClick={toggleExpand}>
                {isExpanded ? 'Thu gọn' : 'Xem tất cả'} 
                <span className="arrow">&gt;</span>
            </button>
          )}
        </div>

        {/* Grid Reviews */}
        <div className="reviews-grid">
          {visibleReviews.length > 0 ? (
            visibleReviews.map((review) => (
                <div key={review.id} className="review-card">
                  {/* 1. Sửa product_name */}
                  <h3 className="product-name">{review.product_name}</h3>
                  
                  {/* Thêm hiển thị sao đánh giá */}
                  <div className="rating" style={{ color: '#ffc107', marginBottom: '5px' }}>
                    {renderStars(review.rating)}
                  </div>

                  <p className="review-content">"{review.content}"</p>
                  
                  <div className="customer-info">
                    {/* 2. Tự tạo Avatar từ tên vì API không có ảnh */}
                    <img 
                        src={`https://ui-avatars.com/api/?name=${encodeURIComponent(review.customer_name)}&background=random&color=fff`} 
                        alt={review.customer_name} 
                        className="avatar" 
                    />
                    
                    <div className="info-text">
                        {/* 3. Sửa customer_name */}
                        <span className="customer-name">{review.customer_name}</span>
                        {/* 4. Thêm hiển thị ngày */}
                        <span className="review-date" style={{ fontSize: '0.8rem', color: '#888', display: 'block' }}>
                            {review.date}
                        </span>
                    </div>
                  </div>
                </div>
            ))
          ) : (
            <p style={{ textAlign: 'center', width: '100%' }}>Chưa có đánh giá nào.</p>
          )}
        </div>

        <div className="reviews-footer-text">
          <p>Chúng tôi luôn trân trọng từng chia sẻ và cảm nhận của bạn — bởi chính những đánh giá chân thành ấy giúp chúng tôi hoàn thiện hơn mỗi ngày.</p>
        </div>

      </div>
    </section>
  );
};

export default CustomerReviews;