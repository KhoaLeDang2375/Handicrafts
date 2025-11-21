import { useState, useEffect } from 'react';
import './CustomerReviews.scss';

// Link API thực tế từ Backend FastAPI
const API_URL = 'http://127.0.0.1:8000/reviews';

const CustomerReviews = () => {
  const [reviews, setReviews] = useState([]);
  const [isExpanded, setIsExpanded] = useState(false); 

  // Lấy dữ liệu từ API
  useEffect(() => {
    const fetchReviews = async () => {
      try {
        const res = await fetch(API_URL);
        if (!res.ok) throw new Error('Kết nối thất bại');
        const data = await res.json();
        
        // Kiểm tra an toàn: chỉ set nếu data là mảng
        // Backend có thể trả về { items: [] } hoặc [] trực tiếp
        const reviewList = Array.isArray(data) ? data : (data.items || []);
        setReviews(reviewList);
        
      } catch (err) {
        console.error("Lỗi tải đánh giá:", err);
        setReviews([]); // Set rỗng để không crash web
      }
    };

    fetchReviews();
  }, []);

  // Logic cắt mảng: Mặc định hiện 3 cái, bấm xem thêm thì hiện hết
  const visibleReviews = isExpanded ? reviews : reviews.slice(0, 3);


  console.log("Dữ liệu reviews hiện tại:", reviews);


  const toggleExpand = () => {
    setIsExpanded(!isExpanded);
  };

  // Hàm render sao đánh giá (Dựa vào field 'rating' hoặc 'ranting' trong DB)
  const renderStars = (rating) => {
    // Chuyển đổi thành số nguyên, mặc định là 5 nếu dữ liệu lỗi
    const numStars = parseInt(rating) || 5; 
    return "★".repeat(numStars); 
  };

  // Hàm format ngày tháng (Dựa vào field 'date' trong DB)
  const formatDate = (dateString) => {
    if (!dateString) return "";
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('vi-VN').format(date); // Ra dạng: 20/11/2025
  };

  return (
    <section className="customer-reviews">
      <div className="reviews-container">
        
        {/* Header */}
        <div className="reviews-header">
          <h2 className="title">Đánh giá từ khách hàng</h2>
        </div>  
        <div className="header-action">
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
                  {/* 1. TÊN SẢN PHẨM 
                     Nếu backend trả về product_name thì dùng, 
                     nếu chỉ có variant_id thì hiển thị tạm ID 
                  */}
                  <h3 className="product-name">
                    {review.product_name || `Sản phẩm #${review.variant_id}`}
                  </h3>
                  
                  {/* 2. SAO ĐÁNH GIÁ */}
                  <div className="rating" style={{ color: '#ffc107', marginBottom: '10px', fontSize: '1.2rem' }}>
                    {/* DB của bạn có thể tên là 'rating' hoặc 'ranting', check cả 2 */}
                    {renderStars(review.rating || review.ranting)}
                  </div>

                  {/* 3. NỘI DUNG ĐÁNH GIÁ */}
                  <p className="review-content">"{review.content}"</p>
                  
                  <div className="customer-info">
                    {/* 4. AVATAR TỰ ĐỘNG 
                        Dùng tên khách hàng để tạo avatar. 
                        Nếu không có tên, dùng customer_id để tạo.
                    */}
                    <img 
                        src={`https://ui-avatars.com/api/?name=${encodeURIComponent(review.customer_name || "User")}&background=random&color=fff`} 
                        alt="avatar" 
                        className="avatar" 
                    />
                    
                    <div className="info-text">
                        {/* 5. TÊN KHÁCH HÀNG */}
                        <span className="customer-name">
                            {review.customer_name || `Khách hàng ${review.customer_id}`}
                        </span>
                        
                        {/* 6. NGÀY ĐÁNH GIÁ */}
                        <span className="review-date" style={{ fontSize: '0.8rem', color: '#888', display: 'block', marginTop: '2px' }}>
                            {formatDate(review.date)}
                        </span>
                    </div>
                  </div>
                </div>
            ))
          ) : (
            <p style={{ textAlign: 'center', width: '100%', color: '#fff' }}>Chưa có đánh giá nào.</p>
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