// src/pages/ProductPage/ProductPage.jsx

import CategoryNav from './CategoryNav';

const ProductPage = () => {
  return (
    <div className="product-page">

      <CategoryNav />

      {/*Đây là nơi chứa sản phẩm */}

      <main className="product-grid-container">
        {/* ... (Code cho lưới sản phẩm sẽ ở đây) ... */}
        <div style={{ height: '2000px', padding: '2rem' }}>
          (Nội dung sản phẩm... cuộn thử để xem hiệu ứng)
        </div>
      </main>

    </div>
  );
};

export default ProductPage;