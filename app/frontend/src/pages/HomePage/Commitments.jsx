// src/pages/HomePage/Commitments.jsx

import './Commitments.scss';

// Dữ liệu cho 3 cột
const commitmentData = [
  {
    title: "VẬT LIỆU TỰ NHIÊN VÀ BỀN VỮNG",
    description: "Chúng tôi sử dụng các vật liệu thân thiện với môi trường như tre, mây, cói biếc, lục bình và tài nguyên tái chế để tạo ra các sản phẩm của mình. Những vật liệu này không chỉ có thể tái tạo... làm cho mỗi sản phẩm trở nên phong cách và bền vững."
  },
  {
    title: "TRỰC TIẾP TỪ NHÀ SẢN XUẤT",
    description: "Chúng tôi là nhà sản xuất ban đầu, không có người trung gian, không có chi phí bổ sung. Bằng cách làm việc trực tiếp với Vietcraft, bạn sẽ nhận được giá cả tốt hơn... kiểm soát chất lượng nhất quán từ xưởng đến giao hàng."
  },
  {
    title: "KINH NGHIỆM XUẤT KHẨU TOÀN CẦU",
    description: "Với hơn một thập kỷ xuất khẩu sang Châu Âu, Châu Mỹ và Châu Á, chúng tôi hiểu các tiêu chuẩn quốc tế, bao bì và hậu cần. Dịch vụ đáng tin cậy... đã nhận được sự tin tưởng của các nhà bán buôn, nhà bán lẻ..."
  }
];

const Commitments = () => {
  return (
    <section className="commitments">
      {/* Container chuẩn để căn giữa */}
      <div className="commitments__container">

        {/* 1. Header của section */}
        <header className="commitments__header">
          <h2 className="title">Đồng hành cùng nghệ nhân Việt</h2>
          <p className="subtitle">
            Mỗi sản phẩm bạn mua không chỉ là một món đồ đẹp, mà còn là sự đóng góp
            vào việc bảo tồn và phát triển làng nghề truyền thống Việt Nam.
          </p>
        </header>

        {/* 2. Lưới 3 cột */}
        <div className="commitments__grid">
          {commitmentData.map((item, index) => (
            <div key={index} className="commitment-item">
              <h3 className="commitment-item__title">{item.title}</h3>
              <p className="commitment-item__description">{item.description}</p>
            </div>
          ))}
        </div>

      </div>
    </section>
  );
};

export default Commitments;