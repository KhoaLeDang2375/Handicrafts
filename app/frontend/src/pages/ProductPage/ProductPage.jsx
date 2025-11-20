// src/pages/ProductPage/ProductPage.jsx

import { useState, useEffect } from 'react';
import CategoryNav from './CategoryNav';
import './ProductPage.scss';
import CustomerReviews from './CustomerReviews';

// Danh sách phân loại (Value phải KHỚP với dữ liệu trong db.json)
const CATEGORIES = [
  { id: 'all', label: 'Tất cả sản phẩm' },
  { id: 1, label: 'Nội thất' },
  { id: 2, label: 'Túi xách' },
  { id: 3, label: 'Thảm' },
  { id: 4, label: 'Trang trí nhà cửa' },
];


// 1. KHAI BÁO URL API
const BASE_URL = 'http://localhost:8000'; 

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

  useEffect(() => {
    const fetchProducts = async () => {
      setIsLoading(true);
      try {
        let url = '';

        if (selectedCategory === 'all') {
           // 1. Gọi API lấy danh sách chung
           // Endpoint: GET /products/
           url = `${BASE_URL}/products`; 
        } else {
           // 2. Gọi API theo ID
           // Endpoint: GET /products/category/{category_id}
           url = `${BASE_URL}/products/category/${selectedCategory}`;
        }

        const response = await fetch(url);
        if (!response.ok) throw new Error('Lỗi kết nối Backend');
        
        const data = await response.json();
        
        // LƯU Ý: Kiểm tra xem Backend trả về mảng luôn hay là object { data: [] }
        // Nếu Swagger trả về trực tiếp list, thì dùng:
        setProducts(data); 

      } catch (err) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };

    fetchProducts();
  }, [selectedCategory]);

  // Tìm trong mảng CATEGORIES xem cái nào có id trùng với selectedCategory
  const currentCategory = CATEGORIES.find(cat => cat.id === selectedCategory);
  
  // Lấy label ra, nếu không tìm thấy (ví dụ lúc mới tải) thì mặc định là 'Tất cả'
  const pageTitle = currentCategory ? currentCategory.label : 'Tất cả sản phẩm';

  return (
    <div className="product-page">
    
      {/* 4. TRUYỀN PROPS XUỐNG CHO CON */}
      <CategoryNav 
        categories={CATEGORIES}
        activeCategory={selectedCategory} 
        onSelectCategory={setSelectedCategory} 
      />

      <div className="product-page__container">

        <header className="product-header">
          <h1 className="product-header__title">
            {pageTitle}
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

      <div style={{ marginTop: '4rem' }}>
        <CustomerReviews />
      </div>
    </div>
  );
};

export default ProductPage;