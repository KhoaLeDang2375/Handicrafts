// Giả sử bạn lưu ảnh mới vào src/assets/images/fiber-hero.png
import fiberImage from '../../assets/images/Fiber-hero.png'; 
import './SlideFiber.scss'; // Tạo file SASS riêng cho slide này

const SlideFiber = () => {
  return (
    <section className="hero-slide hero-slide--fiber">
      <div className="hero-slide__content">
        <span className="hero-slide__subtitle">SẢN PHẨM CỦA CHÚNG TÔI</span>
        <h1 className="hero-slide__title">Đồ gia dụng sợi<br />tự nhiên</h1>
        <p className="hero-slide__description">
          Sản phẩm của chúng tôi được phát triển với thiết kế hiện đại,
          cuộc sống thực tế, chi phí hợp lí và tay nghề thủ công đẹp mắt.
        </p>
        {/* Nút này có style khác, hãy dùng btn--secondary cho giống màu */}
        <button className="btn btn--secondary">TẤT CẢ SẢN PHẨM</button>
      </div>
      <div className="hero-slide__image-container">
        <img src={fiberImage} alt="Đồ gia dụng sợi tự nhiên" />
      </div>
    </section>
  );
};

export default SlideFiber;