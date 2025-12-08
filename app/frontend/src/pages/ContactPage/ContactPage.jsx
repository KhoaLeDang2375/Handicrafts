import React, { useState, useEffect } from 'react';
import './ContactPage.scss';
import { FiPhone, FiMail, FiMap, FiCheck } from 'react-icons/fi';
import { apiCall } from '../../services/api';
import SocialLink from '../../components/layout/SocialLink';
import bannerImg from '../../assets/images/lien-he.jpg';

const ContactPage = () => {
    // State quản lý form
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        content: ''
    });
    const [loading, setLoading] = useState(false);

    // --- 1. Tự động điền thông tin từ LocalStorage ---
    useEffect(() => {
        const storedUser = localStorage.getItem('currentUser');

        if (storedUser) {
            try {
                const user = JSON.parse(storedUser);
                setFormData(prev => ({
                    ...prev,
                    name: user.name || user.full_name || '',
                    email: user.email || ''
                }));
            } catch (error) {
                console.error("Lỗi đọc dữ liệu user:", error);
            }
        }
    }, []);

    // Xử lý thay đổi input
    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    // 2. Xử lý gửi form
    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        try {
            const messageContent = `${formData.content}`;

            const response = await apiCall('/contact/', {
                method: 'POST',
                body: JSON.stringify({ content: messageContent })
            });

            if (response.ok) {
                alert("Gửi thành công!");
                setFormData({ ...formData, content: '' });
            } else {
                alert("Lỗi gửi tin nhắn.");
            }
        } catch (error) {
            console.error(error);
            alert("Lỗi kết nối.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="contact-page">
            {/* 1. Phần Banner */}
            <div
                className="contact-banner"
                style={{ backgroundImage: `url(${bannerImg})` }}
            >
                <div className="banner-overlay">
                    <h1>Liên hệ chúng tôi</h1>
                </div>
            </div>

            {/* 2. Phần Thông Tin Liên Hệ (3 Cột) */}
            <div className="contact-info-section">
                <div className="info-grid">

                    {/* Cột 1: Phone */}
                    <div className="info-item">
                        <div className="icon-circle"><FiPhone /></div>
                        <h3>Phone</h3>
                        <p>+ 84 123 456 789</p>
                    </div>

                    {/* Cột 2: Email */}
                    <div className="info-item">
                        <div className="icon-circle"><FiMail /></div>
                        <h3>Mail</h3>
                        <p>sale@auracraft.com</p>
                    </div>

                    {/* Cột 3: Showroom */}
                    <div className="info-item">
                        <div className="icon-circle"><FiMap /></div>
                        <h3>Showroom</h3>
                        <p>Hồ Chí Minh, Việt Nam</p>
                    </div>

                </div>
            </div>

            {/* --- 3. Form Section --- */}
            <div className="contact-form-wrapper">
                <div className="form-layout partner-section">
                    {/* Cột Trái: Tiêu đề */}
                    <div className="form-title-col">
                        <h2>Trở thành đối tác thương mại của chúng tôi</h2>
                    </div>

                    {/* Cột Phải: Nội dung mô tả  */}
                    <div className="form-input-col">
                        <p className="desc-text">
                            Nền tảng đặt hàng kỹ thuật số này là cách chúng tôi nâng cao trải nghiệm của khách hàng.
                        </p>
                        <p className="desc-text">
                            Khách hàng của chúng tôi có thể duyệt qua hàng trăm sản phẩm tiềm năng,
                            so sánh, chọn các tùy chọn vận chuyển và thanh toán tối ưu, gửi đơn đặt hàng
                            và quản lý mua hàng của họ một cách dễ dàng chỉ với vài cú nhấp chuột.
                            Chúng tôi nghĩ rằng chúng tôi nên bảo tồn truyền thống theo những cách sáng tạo.
                        </p>

                        {/* Danh sách lợi ích */}
                        <div className="benefit-list">
                            {[
                                "Quy trình mua hàng dễ dàng",
                                "So sánh các tùy chọn Vận chuyển",
                                "Đặt hàng nhanh chóng",
                                "Sự đàm phán",
                                "Quản lý trạng thái và lịch sử đơn hàng",
                                "Ưu đãi độc quyền"
                            ].map((item, index) => (
                                <div key={index} className="benefit-item">
                                    <span className="check-icon"><FiCheck /></span>
                                    <span>{item}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Đường kẻ ngăn cách */}
                <div className="divider-line"></div>

                <div className="form-layout">

                    {/* Cột Trái: Tiêu đề */}
                    <div className="form-title-col">
                        <h2>Gửi tin nhắn</h2>
                        <p>Chúng tôi luôn sẵn sàng lắng nghe bạn</p>
                    </div>

                    {/* Cột Phải: Form nhập liệu */}
                    <div className="form-input-col">
                        <form onSubmit={handleSubmit}>

                            <div className="input-group">
                                <label>Họ và tên</label>
                                <p>Họ và tên của bạn</p>
                                <input
                                    type="text"
                                    name="name"
                                    value={formData.name}
                                    onChange={handleChange}
                                    placeholder="Nhập họ tên của bạn" // Placeholder mờ
                                    required
                                />
                            </div>

                            <div className="input-group">
                                <label>Email</label>
                                <p>Địa chỉ email của công ty được ưu tiên hơn.</p>
                                <input
                                    type="email"
                                    name="email"
                                    value={formData.email}
                                    onChange={handleChange}
                                    placeholder="Nhập địa chỉ email"
                                    required
                                />
                            </div>

                            <div className="input-group">
                                <label>Thông điệp</label>
                                <p>Vui lòng cho chúng tôi biết thêm về doanh nghiệp của bạn và bất kỳ câu hỏi nào bạn muốn hỏi.</p>
                                <textarea
                                    name="content"
                                    value={formData.content}
                                    onChange={handleChange}
                                    rows="1" 
                                    required
                                ></textarea>
                            </div>

                            <button type="submit" className="submit-btn-pill" disabled={loading}>
                                {loading ? 'ĐANG GỬI...' : 'GỬI TIN NHẮN'}
                            </button>

                        </form>
                    </div>

                </div>
            </div>

            <SocialLink />
        </div>
    );
};

export default ContactPage;