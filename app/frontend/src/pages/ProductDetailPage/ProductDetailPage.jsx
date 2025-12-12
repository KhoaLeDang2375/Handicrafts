import { useState, useEffect } from 'react';
import { Link, useParams, useNavigate } from 'react-router-dom';
import { getProductById } from '../../services/productApi';
import { apiCall } from '../../services/api';
import { FiPackage, FiShield, FiAward } from "react-icons/fi";
import './ProductDetailPage.scss';
import ProductTabs from './ProductTabs';

import artisan from '../../assets/images/Aura.png';

// 1. CẤU HÌNH CƠ BẢN
const API_BASE = 'http://127.0.0.1:8000';
const DISCOUNT_RATE = 0.2; // Giảm giá mặc định 20% 

const ProductDetailPage = () => {
  const { id } = useParams(); // Lấy ID từ URL (ví dụ: /san-pham/1)
  const navigate = useNavigate();

  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // State cho biến thể và số lượng
  const [quantity, setQuantity] = useState(1);
  const [selectedColor, setSelectedColor] = useState('');
  const [selectedSize, setSelectedSize] = useState('');
  const [currentVariant, setCurrentVariant] = useState(null);
  const [selectedImage, setSelectedImage] = useState('');

  // Hàm format tiền
  const formatCurrency = (amount) =>
    new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(amount);

  // --- GỌI API BACKEND ---
  useEffect(() => {
    const fetchDetail = async () => {
      setLoading(true);
      setError(null);

      try {
        // --- GỌI API RÚT GỌN ---
        const data = await getProductById(id);
        
        setProduct(data);

        // --- XỬ LÝ ẢNH: Backend trả về 'image_url', cần ghép với API_BASE
        const imageUrl = data.image_url 
          ? `${API_BASE}${data.image_url}` 
          : 'https://placehold.co/600x600?text=No+Image';
          
        setSelectedImage(imageUrl);

        // --- XỬ LÝ BIẾN THỂ ---
        if (data.variants && data.variants.length > 0) {
          setSelectedColor(data.variants[0].color || "");
          setSelectedSize(data.variants[0].size || "");
        }

      } catch (err) {
        // api.js đã xử lý message lỗi chuẩn
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    if (id) fetchDetail();
  }, [id]);

  // --- LOGIC TÌM BIẾN THỂ (Khi người dùng chọn màu/size) ---
  useEffect(() => {
    if (product?.variants) {
      const found = product.variants.find(
        v => v.color === selectedColor && v.size === selectedSize
      );
      setCurrentVariant(found || null);
    }
  }, [selectedColor, selectedSize, product]);


  // --- LOGIC TÍNH TOÁN ---
  // Lọc danh sách màu/size duy nhất để tạo Dropdown
  // (Dùng Set để loại bỏ trùng lặp)
  const uniqueColors = product ? [...new Set(product.variants?.map(v => v.color))] : [];
  const uniqueSizes = product ? [...new Set(product.variants?.map(v => v.size))] : [];

  // Tính Rating trung bình
  const reviews = product?.reviews || [];
  const avgRating = reviews.length > 0
    ? reviews.reduce((acc, cur) => acc + (cur.rating || 5), 0) / reviews.length
    : 0;

  // --- XỬ LÝ SỐ LƯỢNG ---
  const handleQuantityChange = (type) => {
    if (type === 'des' && quantity > 1) setQuantity(quantity - 1);
    if (type === 'inc') {
      if (currentVariant && quantity < currentVariant.amount) {
        setQuantity(quantity + 1);
      } else if (!currentVariant) {
        alert("Vui lòng chọn phân loại trước");
      } else {
        alert("Đã đạt giới hạn tồn kho");
      }
    }
  };

  // --- RENDER GIAO DIỆN ---
  if (loading) return <div className="loading-screen">Đang tải chi tiết sản phẩm...</div>;
  if (error) return <div className="error-screen">Lỗi: {error}</div>;
  if (!product) return null;

  // --- HÀM THÊM VÀO GIỎ  ---
  const handleAddToCart = async () => {
    const token = localStorage.getItem('authToken');
    if (!token) {
      alert("Vui lòng đăng nhập để mua hàng!");
      return;
    }

    if (!currentVariant) {
      alert("Vui lòng chọn Màu sắc và Kích thước!");
      return;
    }

    try {
      // Gọi API (Dùng apiCall)
      // apiCall trả về thẳng DATA, nếu lỗi nó sẽ nhảy xuống catch
      const result = await apiCall('/my-cart/add-item', {
        method: 'POST',
        body: JSON.stringify({
          productvariant_id: currentVariant.id,
          product_quantity: quantity,
          access_token: token 
        })
      });

      alert(`Đã thêm ${quantity} sản phẩm vào giỏ hàng!`);
      
      // Console log để kiểm tra kết quả trả về 
      console.log("Kết quả thêm giỏ:", result);

    } catch (error) {
      // apiCall đã xử lý message lỗi chuẩn
      console.error("Lỗi thêm giỏ hàng:", error);
      alert(error.message || "Có lỗi xảy ra khi thêm vào giỏ hàng");
    }
  };

  const handleBuyNow = () => {
    if (!currentVariant) {
      alert("Vui lòng chọn phân loại hàng!");
      return;
    }

    // Tạo object sản phẩm để gửi sang trang thanh toán
    const productToCheckout = {
      product_id: product.id,
      variant_id: currentVariant.id,
      name: product.name,
      color: currentVariant.color,
      size: currentVariant.size,
      price: currentVariant.price, // Giá gốc hoặc giá giảm tùy logic
      quantity: quantity
    };

    // Chuyển trang và mang theo cục dữ liệu này
    navigate('/thanh-toan', { state: { productToBuy: productToCheckout } });
  };

  return (
    <div className="product-detail-page">

      <div className="breadcrumb container">
        <Link to="/san-pham"> &lt; Quay lại danh sách</Link>
      </div>

      <div className="product-container container">
        {/* CỘT TRÁI: ẢNH */}
        <div className="product-gallery">
          <div className="main-image">
            <img src={selectedImage} alt={product.name} />
          </div>
          {/* Nếu backend có danh sách ảnh phụ thì map ở đây, tạm thời để trống hoặc dùng ảnh chính */}
        </div>

        {/* CỘT PHẢI: THÔNG TIN */}
        <div className="product-info">
          {/* Category ID hoặc Name nếu backend join bảng */}
          <span className="category-tag">Danh mục: {product.category_id}</span>

          <h1 className="product-title">{product.name}</h1>

          <div className="product-rating">
            <span className="stars">
              {avgRating > 0 ? "★".repeat(Math.round(avgRating)) : "Chưa có đánh giá"}
            </span>
            {avgRating > 0 && <span className="rating-num">({avgRating.toFixed(1)})</span>}
            <span className="review-count"> · {reviews.length} đánh giá</span>
          </div>

          {/* GIÁ TIỀN & KHUYẾN MÃI */}
          <div className="product-price-box">
            {currentVariant ? (
              <>
                {/* Giá bán = Giá gốc * (1 - %Giảm) */}
                <span className="current-price">
                  {formatCurrency(currentVariant.price * (1 - DISCOUNT_RATE))}
                </span>

                {/* Giá gốc từ DB */}
                <span className="original-price">
                  {formatCurrency(currentVariant.price)}
                </span>

              </>
            ) : (
              <span className="current-price" style={{ fontSize: '1.2rem' }}>
                {product.variants?.length > 0 ? "Vui lòng chọn màu/size" : "Đang cập nhật giá"}
              </span>
            )}
          </div>

          <div className="discount-badge-box">
            <span className="discount-badge">Tiết kiệm {DISCOUNT_RATE * 100}%</span>
          </div>
          <p className="product-description">{product.description}</p>

          {/* THÔNG TIN NGHỆ NHÂN (Từ DB) */}
          {product.artisan_description && (
            <div className="artisan-box">
              {/* Ảnh placeholder cho nghệ nhân */}
              <img src={artisan} alt="Artisan" className="artisan-avatar" />
              <div className="artisan-text">
                <h4>Thông tin nghệ nhân</h4>
                <p>{product.artisan_description}</p>
              </div>
            </div>
          )}

          {/* DROPDOWN CHỌN BIẾN THỂ */}
          {product.variants?.length > 0 && (
            <div className="product-options">
              <div className="option-group">
                <label>Màu sắc</label>
                <select value={selectedColor} onChange={(e) => setSelectedColor(e.target.value)}>
                  {uniqueColors.map((c, idx) => <option key={idx} value={c}>{c}</option>)}
                </select>
              </div>

              <div className="option-group">
                <label>Kích thước</label>
                <select value={selectedSize} onChange={(e) => setSelectedSize(e.target.value)}>
                  {uniqueSizes.map((s, idx) => <option key={idx} value={s}>{s}</option>)}
                </select>
              </div>
            </div>
          )}

          {/* SỐ LƯỢNG & TRẠNG THÁI KHO */}
          <div className="quantity-section">
            <label>Số lượng</label>
            <div className="quantity-control">
              <button onClick={() => handleQuantityChange('des')}>-</button>
              <input type="text" value={quantity} readOnly />
              <button onClick={() => handleQuantityChange('inc')}>+</button>
            </div>

            <span className="stock-status">
              {currentVariant ? (
                currentVariant.amount > 0
                  ? <span className="in-stock">✓ Còn hàng ({currentVariant.amount})</span>
                  : <span className="out-stock">✕ Tạm hết hàng</span>
              ) : (
                <span>---</span>
              )}
            </span>
          </div>

          {/* NÚT MUA HÀNG */}
          <div className="action-buttons">
            <button
              className="btn btn-add-cart"
              disabled={!currentVariant || currentVariant.amount === 0}
              onClick={handleAddToCart}
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="9" cy="21" r="1"></circle><circle cx="20" cy="21" r="1"></circle><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path></svg>
              Thêm vào giỏ hàng
            </button>

            <button
              className="btn btn-buy-now"
              onClick={handleBuyNow}
            // disabled={!currentVariant || currentVariant.amount === 0}
            >
              Mua ngay
            </button>
          </div>

          {/* CHÍNH SÁCH */}
          <div className="policy-grid">

            <div className="policy-item">
              <div className="icon-box">
                <FiPackage size={28} />
              </div>
              <span>Miễn phí vận chuyển</span>
            </div>

            <div className="policy-item">
              <div className="icon-box">
                <FiShield size={28} />
              </div>
              <span>Bảo hành 12 tháng</span>
            </div>

            <div className="policy-item">
              <div className="icon-box">
                <FiAward size={28} />
              </div>
              <span>100% thủ công</span>
            </div>
          </div>

        </div>
      </div>

      <div className="container">
        {/* Truyền dữ liệu xuống: product (lấy category, reviews) và currentVariant (lấy size/color) */}
        <ProductTabs product={product} currentVariant={currentVariant} />
      </div>

    </div>
  );
};

export default ProductDetailPage;