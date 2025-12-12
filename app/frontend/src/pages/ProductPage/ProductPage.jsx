import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import CategoryNav from './CategoryNav';
import './ProductPage.scss';
import CustomerReviews from './CustomerReviews';

import { getAllProducts } from '../../services/productApi';
import { addToCart } from '../../services/cartApi';

// 1. KHAI BÁO URL BACKEND
const API_BASE = 'http://127.0.0.1:8000';

const ProductPage = () => {
  // Danh sách sản phẩm gốc từ backend
  const [products, setProducts] = useState([]);

  // Danh sách sản phẩm sau khi lọc theo category
  const [filteredProducts, setFilteredProducts] = useState([]);

  // Danh mục
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('all');

  // State loading và error
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  // Hàm format tiền tệ
  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(amount);
  };

  // GỌI API
  useEffect(() => {
    const fetchProductsAndCategories = async () => {
      setIsLoading(true);
      // Reset lỗi cũ trước khi gọi mới
      setError(null);

      try {
        // Hàm này trả về thẳng dữ liệu (data)
        const data = await getAllProducts();

        console.log('Data từ backend:', data);

        // --- LOGIC XỬ LÝ DỮ LIỆU ---
        const productList = data.items || [];

        setProducts(productList);

        // Tạo danh mục từ dữ liệu
        const categorySet = new Set(productList.map((p) => p.category_name));
        const normalizedCategories = Array.from(categorySet).map((cat, index) => ({
          id: index + 1,
          label: cat || 'Khác',
          value: cat,
        }));

        setCategories([{ id: 'all', label: 'Tất cả sản phẩm', value: 'all' }, ...normalizedCategories]);
        setFilteredProducts(productList);

      } catch (err) {
        // apiCall đã ném ra Error với message chuẩn
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };

    fetchProductsAndCategories();
  }, []);

  // Lọc sản phẩm theo danh mục
  useEffect(() => {
    console.log('--- BẮT ĐẦU LỌC ---');
    console.log('Danh mục đang chọn (selectedCategory):', selectedCategory);
    console.log('Tổng sản phẩm gốc (products):', products.length);

    if (selectedCategory === 'all') {
      setFilteredProducts(products);
    } else {
      // Log thử xem so sánh có khớp không
      const result = products.filter((p) => {
        const isMatch = p.category_id === selectedCategory;
        // Nếu tên danh mục trong sản phẩm khác tên danh mục đang chọn -> in ra để biết
        if (!isMatch && products.indexOf(p) === 0) {
          console.log(`So sánh mẫu: "${p.category_name}" (Sản phẩm) !== "${selectedCategory}" (Đang chọn)`);
        }
        return isMatch;
      });

      console.log(`Kết quả lọc: tìm thấy ${result.length} sản phẩm`);
      setFilteredProducts(result);
    }
  }, [selectedCategory, products]);

  // Xác định tiêu đề trang
  const currentCategory = categories.find((cat) => cat.value === selectedCategory);
  const pageTitle = currentCategory ? currentCategory.label : 'Tất cả sản phẩm';

  // --- HÀM XỬ LÝ THÊM VÀO GIỎ ---
  const handleAddToCart = async (product) => {
    // 1. Kiểm tra đăng nhập
    const token = localStorage.getItem('authToken');
    if (!token) {
      alert("Vui lòng đăng nhập để mua hàng!");
      // Hoặc chuyển hướng sang trang login: navigate('/login');
      return;
    }
    console.log("Token đang dùng:", token);

    // 2. Lấy ID của biến thể (Variant) đầu tiên
    // Vì ở trang danh sách ta không chọn size/màu, nên mặc định lấy cái đầu tiên
    const firstVariant = product.variants && product.variants.length > 0 ? product.variants[0] : null;

    if (!firstVariant) {
      alert("Sản phẩm này đang lỗi dữ liệu (chưa có biến thể).");
      return;
    }

    // 3. Gọi API
    try {
      await addToCart(firstVariant.id, 1, token);
      alert("Thêm sản phẩm thành công!");

    } catch (error) {
      console.error("Lỗi:", error);
    }
  };


  return (
    <div className="product-page">
      {/* TRUYỀN DỮ LIỆU XUỐNG CategoryNav */}
      <CategoryNav
        categories={categories}
        activeCategory={selectedCategory}
        onSelectCategory={(value) => setSelectedCategory(value)}
      />

      <div className="product-page__container">
        <header className="product-header">
          <h1 className="product-header__title">{pageTitle}</h1>
          <p className="product-header__count">{filteredProducts.length} sản phẩm thủ công độc đáo</p>
        </header>

        {isLoading ? (
          <div className="loading">Đang tải sản phẩm...</div>
        ) : error ? (
          <div className="error">Lỗi: {error} (Hãy kiểm tra lại backend)</div>
        ) : (
          <div className="product-grid">
            {/* Xử lý trường hợp không có sản phẩm nào */}
            {filteredProducts.length === 0 && (
              <div style={{ gridColumn: '1 / -1', textAlign: 'center', padding: '2rem', color: '#666' }}>
                Không tìm thấy sản phẩm nào trong danh mục này.
              </div>
            )}

            {filteredProducts.map((product) => {
              // Logic lấy GIÁ và ẢNH an toàn

              // Lấy giá từ variant đầu tiên, nếu không có set bằng 0
              const displayPrice = product.variants?.length > 0 ? product.variants[0].price : 0;

              // Kiểm tra nếu có image_url từ backend thì ghép với API_BASE
              // Nếu không có thì dùng ảnh placeholder
              const displayImage = product.image_url
                ? `${API_BASE}${product.image_url}`
                : 'https://placehold.co/400x400?text=No+Image';

              // Kiểm tra trạng thái còn hàng
              const isOutOfStock = product.status && product.status.toLowerCase() === 'out of stock';

              return (
                <Link to={`/san-pham/${product.id}`} key={product.id} className="product-card">
                  <div className="product-card__image">
                    <img
                      src={displayImage}
                      alt={product.name}
                      // Nếu ảnh lỗi thì load ảnh dự phòng
                      onError={(e) => { e.target.src = 'https://placehold.co/400x400?text=No+Image' }}
                    />
                    {/* Badge trạng thái */}
                    {isOutOfStock && <span className="status-badge out-of-stock">Hết hàng</span>}
                  </div>

                  <div className="product-card__content">
                    <h3 className="product-name">{product.name}</h3>

                    {/* Cắt ngắn mô tả cho gọn giao diện */}
                    <p className="product-desc">
                      {product.description && product.description.length > 60
                        ? product.description.substring(0, 60) + '...'
                        : product.description}
                    </p>

                    <div className="product-price">{formatCurrency(displayPrice)}</div>

                    <button
                      className="add-to-cart-btn btn--primary"
                      disabled={isOutOfStock}
                      style={{ opacity: isOutOfStock ? 0.5 : 1, cursor: isOutOfStock ? 'not-allowed' : 'pointer' }}

                      onClick={(e) => {
                        e.preventDefault(); // Ngăn chặn Link bao ngoài (nếu có) nhảy trang
                        handleAddToCart(product);
                      }}
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="16"
                        height="16"
                        fill="currentColor"
                        viewBox="0 0 16 16"
                      >
                        <path d="M0 1.5A.5.5 0 0 1 .5 1H2a.5.5 0 0 1 .485.379L2.89 3H14.5a.5.5 0 0 1 .491.592l-1.5 8A.5.5 0 0 1 13 12H4a.5.5 0 0 1-.491-.408L2.01 3.607 1.61 2H.5a.5.5 0 0 1-.5-.5zM3.102 4l1.313 7h8.17l1.313-7H3.102zM5 12a2 2 0 1 0 0 4 2 2 0 0 0 0-4zm7 0a2 2 0 1 0 0 4 2 2 0 0 0 0-4z" />
                      </svg>
                      {isOutOfStock ? 'Tạm hết hàng' : 'Thêm vào giỏ'}
                    </button>
                  </div>
                </Link>
              );
            })}
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