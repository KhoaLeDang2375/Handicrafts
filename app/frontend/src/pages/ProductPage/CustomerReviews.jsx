import { useState, useEffect } from 'react';
import './CustomerReviews.scss';

// Link API giả lập (JSON Server)
const API_URL = 'http://localhost:8000/reviews';

const CustomerReviews = () => {
  const [reviews, setReviews] = useState([]);
  const [isExpanded, setIsExpanded] = useState(false); // State quản lý trạng thái mở rộng

  // Lấy dữ liệu từ API
  useEffect(() => {
    fetch(API_URL)
      .then(res => res.json())
      .then(data => setReviews(data))
      .catch(err => console.error("Lỗi tải đánh giá:", err));
  }, []);

  // Logic cắt mảng: Nếu mở rộng thì lấy hết, nếu không thì lấy 3 cái đầu
  const visibleReviews = isExpanded ? reviews : reviews.slice(0, 3);

  const toggleExpand = () => {
    setIsExpanded(!isExpanded);
  };

  return (
    <section className="customer-reviews">
      <div className="reviews-container">
        
        {/* Header */}
        <div className="reviews-header">
          <h2 className="title">Đánh giá</h2>
          <button className="toggle-btn" onClick={toggleExpand}>
            {isExpanded ? 'Thu gọn' : 'Tất cả đánh giá'} 
            <span className="arrow">&gt;</span>
          </button>
        </div>

        {/* Grid Reviews */}
        <div className="reviews-grid">
          {visibleReviews.map((review) => (
            <div key={review.id} className="review-card">
              <h3 className="product-name">Sản phẩm: {review.productName}</h3>
              <p className="review-content">"{review.content}"</p>
              
              <div className="customer-info">
                <img src={review.avatar} alt={review.customerName} className="avatar" />
                <span className="customer-name">{review.customerName}</span>
              </div>
            </div>
          ))}
        </div>

        <div className="reviews-footer-text">
          <p>Chúng tôi luôn trân trọng từng chia sẻ và cảm nhận của bạn — bởi chính những đánh giá chân thành ấy giúp chúng tôi hoàn thiện hơn mỗi ngày, để mang đến những trải nghiệm tốt hơn trong mỗi lần bạn quay lại.</p>
        </div>

      </div>
    </section>
  );
};

export default CustomerReviews;