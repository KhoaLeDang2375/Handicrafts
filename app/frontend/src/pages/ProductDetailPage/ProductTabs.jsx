import { useState } from 'react';
import './ProductTabs.scss';

const ProductTabs = ({ product, currentVariant }) => {
  const [activeTab, setActiveTab] = useState('details'); // 'details' hoặc 'reviews'

  // Dữ liệu tĩnh theo yêu cầu của bạn
  const staticInfo = {
    origin: "Bát Tràng, Hồ Chí Minh",
    tech: "Công nghệ cao",
    story: "Mỗi chiếc bình gốm đều là một tác phẩm nghệ thuật độc đáo, được tạo nên từ bàn tay tài hoa của nghệ nhân. Họa tiết hoa sen được vẽ tay tỉ mỉ, mang ý nghĩa thanh cao, thuần khiết trong văn hóa phương Đông. Sản phẩm không chỉ là vật dụng trang trí mà còn là sự kết tinh của nghề truyền thống Bát Tràng hàng trăm năm tuổi."
  };

  // Hàm render sao
  const renderStars = (rating) => "★".repeat(rating || 5);

  // Hàm format ngày
  const formatDate = (dateString) => {
    if (!dateString) return "";
    return new Intl.DateTimeFormat('vi-VN').format(new Date(dateString));
  };

  return (
    <div className="product-tabs">
      {/* 1. HEADER TABS */}
      <div className="tabs-header">
        <button 
          className={`tab-btn ${activeTab === 'details' ? 'active' : ''}`}
          onClick={() => setActiveTab('details')}
        >
          Chi tiết sản phẩm
        </button>
        <button 
          className={`tab-btn ${activeTab === 'reviews' ? 'active' : ''}`}
          onClick={() => setActiveTab('reviews')}
        >
          Đánh giá ({product.reviews ? product.reviews.length : 0})
        </button>
      </div>

      {/* 2. CONTENT BODY */}
      <div className="tabs-content">
        
        {/* --- TAB CHI TIẾT --- */}
        {activeTab === 'details' && (
          <div className="details-panel">
            <h3 className="section-title">Thông tin sản phẩm</h3>
            <ul className="info-list">
              <li>
                <strong>Chất liệu:</strong> {product.category_name || "Gốm sứ cao cấp"}
              </li>
              <li>
                <strong>Kích thước:</strong> {currentVariant ? currentVariant.size : "Theo phân loại"}
              </li>
              <li>
                <strong>Màu sắc:</strong> {currentVariant ? currentVariant.color : "Theo phân loại"}
              </li>
              <li>
                <strong>Xuất xứ:</strong> {staticInfo.origin}
              </li>
              <li>
                <strong>Công nghệ:</strong> {staticInfo.tech}
              </li>
            </ul>

            <div className="product-story">
              <h3 className="section-title">Câu chuyện sản phẩm</h3>
              <p>{staticInfo.story}</p>
            </div>
          </div>
        )}

        {/* --- TAB ĐÁNH GIÁ --- */}
        {activeTab === 'reviews' && (
          <div className="reviews-panel">
            {product.reviews && product.reviews.length > 0 ? (
              <div className="review-list">
                {product.reviews.map((review, index) => (
                  <div key={review.id || index} className="review-item">
                    <div className="review-header">
                      <span className="author">{review.customer_name || "Khách hàng ẩn danh"}</span>
                      <span className="date">{formatDate(review.date)}</span>
                    </div>
                    <div className="rating-stars">{renderStars(review.rating)}</div>
                    <p className="content">{review.content}</p>
                  </div>
                ))}
              </div>
            ) : (
              <p className="no-reviews">Chưa có đánh giá nào cho sản phẩm này.</p>
            )}
          </div>
        )}

      </div>
    </div>
  );
};

export default ProductTabs;