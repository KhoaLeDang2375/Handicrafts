// src/pages/HomePage/OurJourney.jsx

import './OurJourney.scss';
import Logo from '../../assets/images/Aura2.png'; 

const journeyData = [
  {
    year: "1985",
    title: "Khởi nguồn từ làng nghề",
    description: "Bắt đầu từ một xưởng nhỏ tại làng gốm Bát Tràng, chúng tôi kế thừa tinh hoa thủ công truyền thống."
  },
  {
    year: "1995",
    title: "Mở rộng quy mô",
    description: "Phát triển thêm các sản phẩm dệt may và đồ gỗ thủ công, hợp tác với nhiều làng nghề Việt Nam."
  },
  {
    year: "2005",
    title: "Ra mắt thương hiệu",
    description: "Chính thức thành lập thương hiệu 'Aura', đưa sản phẩm làng nghề đến gần hơn với người tiêu dùng."
  },
  {
    year: "2015",
    title: "Hướng đến quốc tế",
    description: "Xuất khẩu sản phẩm thủ công Việt Nam ra thị trường quốc tế, mang tinh hoa văn hóa đến toàn cầu."
  },
  {
    year: "2025",
    title: "Tương lai bền vững",
    description: "Cam kết phát triển bền vững, bảo tồn làng nghề truyền thống và tạo sinh kế cho nghệ nhân."
  }
];

const OurJourney = () => {
  return (
    <section className="our-journey">

      <div className="journey-separator">
        <div className="our-journey__container">
          <div className="logo-mask"> 
            <img src={Logo} alt="Aura Logo" className="journey-logo" />
          </div>
          {/* Đường line sẽ được tạo bằng CSS */}
        </div>
      </div>

      <div className="journey-part journey-part--bottom">
        <div className="our-journey__container">
          <header className="our-journey__header">
            <h2 className="title">Hành trình của chúng tôi</h2>
            <p className="subtitle">
              40 năm gìn giữ và phát huy tinh hoa thủ công truyền thống Việt Nam
            </p>
          </header>

          {/* Timeline */}
          <div className="timeline">
            {journeyData.map((item, index) => (
              <div key={index} className="timeline-item">
                <div className="timeline-content">
                  <span className="timeline-year">{item.year}</span>
                  <h3 className="timeline-title">{item.title}</h3>
                  <p className="timeline-description">{item.description}</p>
                </div>
              </div>
            ))}
          </div>

        </div>
      </div>

    </section>
  );
};

export default OurJourney;