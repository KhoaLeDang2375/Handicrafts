// src/pages/HomePage/FeaturedProducts.jsx

import './FeaturedProducts.scss';

// 1. Import 3 ảnh của bạn
import imgNoiThat from '../../assets/images/noi-that.png';
import imgTuiXach from '../../assets/images/tui-xach.png';
import imgTrangTri from '../../assets/images/trang-tri.png';

const FeaturedProducts = () => {
    return (
        <section className="featured-products">
            <div className="featured-products__container">
                <div className="featured-products__header">
                    <span className="subtitle">Sản phẩm với tình yêu và tâm huyết</span>
                    <h2 className="title">Sản phẩm nổi bật</h2>
                </div>

                <div className="featured-products__grid">
                    {/* Card 1: Nội thất */}
                    <div className="product-card">
                        <div className="product-card__image-wrapper">
                            <img src={imgNoiThat} alt="Nội thất" />
                        </div>
                        <h3 className="product-card__caption">Nội thất</h3>
                    </div>

                    {/* Card 2: Túi xách */}
                    <div className="product-card">
                        <div className="product-card__image-wrapper">
                            <img src={imgTuiXach} alt="Túi xách" />
                        </div>
                        <h3 className="product-card__caption">Túi xách</h3>
                    </div>

                    {/* Card 3: Trang trí */}
                    <div className="product-card">
                        <div className="product-card__image-wrapper">
                            <img src={imgTrangTri} alt="Trang trí" />
                        </div>
                        <h3 className="product-card__caption">Trang trí</h3>
                    </div>
                </div>

                <div className="featured-products__footer">
                    {/* Nút này dùng class "btn--primary" màu cam */}
                    {/* Hiệu ứng hover đen sẽ tự động áp dụng nếu bạn đã setup mixin */}
                    <button className="btn btn--secondary">TẤT CẢ SẢN PHẨM</button>
                </div>
            </div>
        </section>
    );
};

export default FeaturedProducts;