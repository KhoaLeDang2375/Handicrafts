// src/pages/HomePage/SlideFair.jsx

import fairImage from '../../assets/images/Fair-background.png'; 
import './SlideFair.scss'; 

const SlideFair = () => {
  return (
    <section
      className="hero-slide hero-slide--fair"
      // 2. Áp dụng ảnh nền bằng style inline 
      style={{ backgroundImage: `url(${fairImage})` }}
    >
      {/* 3. Đây là lớp nội dung sẽ nằm bên trên */}
      <div className="hero-slide__content">
        <span className="hero-slide__subtitle">HỘI CHỢ THƯƠNG MẠI</span>
        <h1 className="hero-slide__title">Gặp chúng tôi tại<br />Lifestyle Fair 2025</h1>
        <p className="hero-slide__description">
          Từ ngày 15 - 20/10/2025 tại sảnh B9.02 - Gian hàng
          IE104 tại UIT Thành phố Hồ Chí Minh, Việt Nam.
        </p>
        
        {/* Dùng lại style nút của slide 1 */}
        <button className="btn btn--secondary">CHI TIẾT HỘI CHỢ</button>
      </div>
    </section>
  );
};

export default SlideFair;