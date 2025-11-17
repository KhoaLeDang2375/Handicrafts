import heroImage from '../../assets/images/HomePage-hero.jpg';
import './SlideAura.scss'; // Tạo file SASS riêng cho slide này

const SlideAura = () => {
  return (
    <section className="hero-slide hero-slide--aura">
      <div className="hero-slide__content">
        <span className="hero-slide__subtitle">CÂU CHUYỆN CỦA CHÚNG TÔI</span>
        <h1 className="hero-slide__title">Một tư duy của <br /> thủ công mỹ nghệ</h1>
        <p className="hero-slide__description">
          AURA - sự "Độc đáo" (Unique) và "Hiếm có" (Rare) trong
          "Nghệ thuật" (Artistry) của người nghệ nhân (Artisan).
        </p>
        <button className="btn btn--secondary">VỀ CHÚNG TÔI</button>
      </div>
      <div className="hero-slide__image-container">
        <img src={heroImage} alt="Cửa hàng thủ công mỹ nghệ Aura" />
      </div>
    </section>
  );
};

export default SlideAura;