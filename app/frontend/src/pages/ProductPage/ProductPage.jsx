// src/pages/ProductPage/ProductPage.jsx

import { useState, useEffect } from 'react';
import CategoryNav from './CategoryNav';
import './ProductPage.scss';

// 1. KHAI BÁO URL API
const API_URL = 'http://localhost:8000/products'; 

const ProductPage = () => {
  // State lưu trữ danh sách sản phẩm
  const [products, setProducts] = useState([]);
  // State trạng thái tải (loading)
  const [isLoading, setIsLoading] = useState(true);
  // State lưu lỗi (nếu có)
  const [error, setError] = useState(null);

  // Hàm format tiền tệ Việt Nam
  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(amount);
  };

  const [selectedCategory, setSelectedCategory] = useState('all');

  // Gọi API
  useEffect(() => {
    const fetchProducts = async () => {
      setIsLoading(true); // Bật loading mỗi khi đổi category
      try {
        // 2. XÂY DỰNG URL DỰA TRÊN CATEGORY
        // Nếu là 'all' thì lấy hết, ngược lại thì thêm ?category=...
        // JSON Server hỗ trợ lọc bằng cách thêm ?tên_trường=giá_trị
        let url = API_URL;
        if (selectedCategory !== 'all') {
           // Ví dụ: http://localhost:8000/products?category=Nội thất
           url += `?category=${selectedCategory}`; 
        }

        const response = await fetch(url);
        if (!response.ok) throw new Error('Kết nối thất bại');
        const data = await response.json();
        setProducts(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };

    fetchProducts();
    
    // 3. Thêm selectedCategory vào dependency array
    // Khi selectedCategory thay đổi, chạy lại useEffect
  }, [selectedCategory]);

  return (
    <div className="product-page">
    
      {/* 4. TRUYỀN PROPS XUỐNG CHO CON */}
      <CategoryNav 
        activeCategory={selectedCategory} 
        onSelectCategory={setSelectedCategory} 
      />

      <div className="product-page__container">

        <header className="product-header">
          <h1 className="product-header__title">
            {selectedCategory === 'all' ? 'Tất cả sản phẩm' : selectedCategory}
          </h1>
          
          <p className="product-header__count">
            {products.length} sản phẩm thủ công độc đáo
          </p>
        </header>

        {/* PHẦN 2: NỘI DUNG CHÍNH */}
        {isLoading ? (
          <div className="loading">Đang tải sản phẩm...</div>
        ) : error ? (
          <div className="error">Lỗi: {error} (Hãy kiểm tra lại backend)</div>
        ) : (
          
          /* LƯỚI SẢN PHẨM (GRID) */
          <div className="product-grid">
            {products.map((product) => (
              <div key={product.id} className="product-card">
                
                {/* Hình ảnh */}
                <div className="product-card__image">
                  <img src={product.image} alt={product.name} />
                </div>

                {/* Thông tin */}
                <div className="product-card__content">
                  <h3 className="product-name">{product.name}</h3>
                  <p className="product-desc">{product.description}</p>
                  <div className="product-price">{formatCurrency(product.price)}</div>
                  
                  {/* Nút thêm vào giỏ */}
                  <button className="add-to-cart-btn btn--primary">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                      <path d="M0 1.5A.5.5 0 0 1 .5 1H2a.5.5 0 0 1 .485.379L2.89 3H14.5a.5.5 0 0 1 .491.592l-1.5 8A.5.5 0 0 1 13 12H4a.5.5 0 0 1-.491-.408L2.01 3.607 1.61 2H.5a.5.5 0 0 1-.5-.5zM3.102 4l1.313 7h8.17l1.313-7H3.102zM5 12a2 2 0 1 0 0 4 2 2 0 0 0 0-4zm7 0a2 2 0 1 0 0 4 2 2 0 0 0 0-4z"/>
                    </svg>
                    Thêm vào giỏ
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

    </div>
  );
};

export default ProductPage;