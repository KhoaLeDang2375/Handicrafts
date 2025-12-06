import React from 'react';
import { Link } from 'react-router-dom';
import './AboutPage.scss';
import { FiHeart, FiUsers, FiAward, FiStar, FiChevronRight } from 'react-icons/fi';

import bannerImg from '../../assets/images/about-banner.jpg';
import storyImg from '../../assets/images/about-story.jpg';
import artisan1 from '../../assets/images/img-login-1.jpg';
import artisan2 from '../../assets/images/artisan2.jpg';
import artisan3 from '../../assets/images/img-login-2.jpg';

// Mock Data cho nghệ nhân
const artisans = [
    {
        id: 1,
        name: "Nguyễn Văn Ming",
        role: "Nghệ nhân mộc",
        experience: "25 năm kinh nghiệm",
        image: artisan1
    },
    {
        id: 2,
        name: "Trần Thị Mai",
        role: "Nghệ nhân gốm",
        experience: "18 năm kinh nghiệm",
        image: artisan2
    },
    {
        id: 3,
        name: "Lê Văn Hùng",
        role: "Nghệ nhân điêu khắc",
        experience: "30 năm kinh nghiệm",
        image: artisan3
    }
];

const AboutPage = () => {
    return (
        <div className="about-page">
            {/* 1. Phần Banner */}
            <div
                className="about-banner"
                style={{ backgroundImage: `url(${bannerImg})` }}
            >
                <div className="banner-overlay">
                    <div className="banner-content">
                        <h1>Về Chúng Tôi</h1>
                        <p>
                            Nơi hội tụ tinh hoa nghệ thuật thủ công truyền thống Việt Nam,
                            mang đến những sản phẩm mỹ nghệ độc đáo và giá trị
                        </p>
                    </div>
                </div>
            </div>

            {/* 2. Phần Câu chuyện*/}
            <div className="about-container">
                <div className="story-section">
                    {/* Cột trái: Nội dung text */}
                    <div className="story-text">
                        <h2>Câu Chuyện Của Chúng Tôi</h2>

                        <p>
                            Được thành lập từ năm 2010, chúng tôi bắt đầu với niềm đam mê
                            bảo tồn và phát triển nghệ thuật thủ công truyền thống Việt Nam.
                            Từ một xưởng nhỏ với vài nghệ nhân, chúng tôi đã phát triển thành
                            một cộng đồng rộng lớn với hơn 50 nghệ nhân tài năng.
                        </p>

                        <p>
                            Mỗi sản phẩm của chúng tôi không chỉ là một món đồ trang trí, mà
                            còn là câu chuyện về văn hóa, con người và tâm hồn Việt Nam.
                            Chúng tôi tin rằng trong mỗi đường nét, mỗi họa tiết đều chứa đựng
                            tình yêu và tâm huyết của người làm ra nó.
                        </p>

                        <p>
                            Sứ mệnh của chúng tôi là mang những giá trị văn hóa truyền
                            thống đến gần hơn với cuộc sống hiện đại, tạo ra những sản phẩm
                            vừa mang tính thẩm mỹ cao vừa có ý nghĩa sâu sắc.
                        </p>
                    </div>

                    {/* Cột phải: Hình ảnh */}
                    <div className="story-image">
                        <img src={storyImg} alt="Bộ sưu tập gốm sứ" />
                    </div>
                </div>
            </div>

            {/* 3. Phần Giá Trị Cốt Lõi */}
            <div className="core-values-section">
                <div className="section-header">
                    <h2>Giá Trị Cốt Lõi</h2>
                    <p className="sub-title">
                        Những giá trị định hướng mọi hoạt động và sản phẩm của chúng tôi
                    </p>
                </div>

                <div className="values-grid">
                    {/* Card 1: Tâm Huyết */}
                    <div className="value-card">
                        <div className="icon-box">
                            <FiHeart />
                        </div>
                        <h3>Tâm Huyết</h3>
                        <p>
                            Mỗi sản phẩm được tạo ra với tình yêu và sự tận tâm của nghệ nhân
                        </p>
                    </div>

                    {/* Card 2: Cộng Đồng */}
                    <div className="value-card">
                        <div className="icon-box">
                            <FiUsers />
                        </div>
                        <h3>Cộng Đồng</h3>
                        <p>
                            Hỗ trợ và phát triển nghề thủ công truyền thống của địa phương
                        </p>
                    </div>

                    {/* Card 3: Chất Lượng */}
                    <div className="value-card">
                        <div className="icon-box">
                            <FiAward />
                        </div>
                        <h3>Chất Lượng</h3>
                        <p>
                            Cam kết chất lượng cao với từng chi tiết được chăm chút tỉ mỉ
                        </p>
                    </div>

                    {/* Card 4: Độc Đáo */}
                    <div className="value-card">
                        <div className="icon-box">
                            <FiStar />
                        </div>
                        <h3>Độc Đáo</h3>
                        <p>
                            Mỗi sản phẩm đều mang dấu ấn riêng, không có hai món giống nhau
                        </p>
                    </div>
                </div>
            </div>

            {/* 4. Phần Quy Trình Sản Xuất */}
            <div className="production-process-section">
                <div className="section-header">
                    <h2>Quy Trình Sản Xuất</h2>
                    <p className="sub-title">
                        Từ nguyên liệu đến thành phẩm, mỗi bước đều được thực hiện với sự tỉ mỉ và chuyên nghiệp
                    </p>
                </div>

                <div className="process-steps">
                    {/* Định nghĩa dữ liệu các bước */}
                    {[
                        {
                            id: 1,
                            title: "Chọn nguyên liệu",
                            desc: "Tuyển chọn nguyên liệu tự nhiên, thân thiện môi trường"
                        },
                        {
                            id: 2,
                            title: "Thiết kế",
                            desc: "Sáng tạo các mẫu mã độc đáo kết hợp truyền thống và hiện đại"
                        },
                        {
                            id: 3,
                            title: "Chế tác",
                            desc: "Nghệ nhân làm thủ công từng sản phẩm với kỹ thuật truyền thống"
                        },
                        {
                            id: 4,
                            title: "Hoàn Thiện",
                            desc: "Kiểm tra chất lượng và hoàn thiện từng chi tiết nhỏ nhất"
                        }
                    ].map((step, index, array) => (
                        <React.Fragment key={step.id}>
                            {/* Thẻ hiển thị từng bước */}
                            <div className="step-item">
                                <div className="step-number">{step.id}</div>
                                <h3>{step.title}</h3>
                                <p>{step.desc}</p>
                            </div>

                            {/* Logic hiển thị mũi tên: Chỉ hiện nếu KHÔNG PHẢI là phần tử cuối cùng */}
                            {index < array.length - 1 && (
                                <div className="step-arrow">
                                    <FiChevronRight />
                                </div>
                            )}
                        </React.Fragment>
                    ))}
                </div>
            </div>


            {/* 5. Phần Đội Ngũ Nghệ Nhân */}
            <div className="team-section">
                <div className="section-header">
                    <h2>Đội Ngũ Nghệ Nhân</h2>
                    <p className="sub-title">
                        Những bàn tay tài hoa tạo nên những sản phẩm mỹ nghệ tinh tế
                    </p>
                </div>

                {/* Link xem tất cả */}
                <div className="team-action-row">
                    <a href="#" className="view-all-link">
                        Xem tất cả nghệ nhân <FiChevronRight />
                    </a>
                </div>

                {/* Grid danh sách nghệ nhân */}
                <div className="team-grid">
                    {artisans.map((person) => (
                        <div key={person.id} className="artisan-card">
                            <div className="card-image">
                                <img src={person.image} alt={person.name} />
                            </div>
                            <div className="card-info">
                                <h3>{person.name}</h3>
                                <p className="role">{person.role}</p>
                                <p className="exp">{person.experience}</p>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* 6. Phần Khám Phá Sản Phẩm */}
            <div className="product-discovery-section">
                <div className="cta-content">
                    <h2>Khám phá sản phẩm của chúng tôi</h2>
                    <p>
                        Mỗi sản phẩm là một tác phẩm nghệ thuật độc đáo, được tạo ra bởi đôi bàn tay khéo léo và tâm hồn đam mê
                    </p>

                    <Link to="/san-pham" className="btn btn--secondary">
                        XEM SẢN PHẨM
                    </Link>
                </div>
            </div>

        </div>
    );
};

export default AboutPage;