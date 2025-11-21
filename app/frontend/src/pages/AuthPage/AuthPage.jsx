import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './AuthPage.scss';

// Import ảnh trang trí
import imgPottery1 from '../../assets/images/img-login-1.jpg';
import imgPottery2 from '../../assets/images/img-login-2.jpg';
import imgPottery3 from '../../assets/images/img-login-3.jpg';

// URL Backend thật (Python FastAPI)
const API_BASE = 'http://127.0.0.1:8000';

const AuthPage = () => {
  // State chuyển đổi Login/Signup
  const [isLogin, setIsLogin] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const [agreeTerms, setAgreeTerms] = useState(false);

  // State lưu dữ liệu form
  const [formData, setFormData] = useState({
    name: '',           // Cho đăng ký
    username: '',       // Cho đăng ký & đăng nhập (Login dùng field này để chứa user hoặc email)
    email: '',          // Cho đăng ký
    phone_number: '',   // Cho đăng ký 
    address: '',        // Cho đăng ký 
    password: '',       // Chung
    confirmPassword: '' // Cho đăng ký
  });

  const navigate = useNavigate();

  // Hàm xử lý nhập liệu
  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  // --- XỬ LÝ ĐĂNG KÝ (Connect to /register/signup) ---
  const handleRegister = async (e) => {
    e.preventDefault();

    if (!agreeTerms) {
      alert("Vui lòng đồng ý với Điều khoản và Chính sách để tiếp tục!");
      return;
    }
    // 1. Validate cơ bản
    if (formData.password !== formData.confirmPassword) {
      alert("Mật khẩu xác nhận không khớp!");
      return;
    }

    setIsLoading(true);
    try {
      // 2. Gọi API Backend
      const response = await fetch(`${API_BASE}/register/signup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: formData.name,
          email: formData.email,
          username: formData.username, // Backend cần field này riêng
          password: formData.password,
          phone_number: formData.phone_number,
          address: formData.address
        })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Đăng ký thất bại");
      }

      // 3. Thành công
      alert("Đăng ký thành công! Vui lòng đăng nhập.");
      setIsLogin(true); // Chuyển sang form Login
      // Reset form password
      setFormData(prev => ({ ...prev, password: '', confirmPassword: '' }));

    } catch (error) {
      alert(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  // --- XỬ LÝ ĐĂNG NHẬP (Connect to /login/) ---
  const handleLogin = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      // 1. Gọi API Login
      const response = await fetch(`${API_BASE}/login/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: formData.username, // Người dùng nhập Email hoặc Username vào đây
          password: formData.password,
          role: "customer" // Bắt buộc phải có để Backend phân loại
        })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Đăng nhập thất bại");
      }

      // 2. Lưu Token vào LocalStorage
      // (Lưu ý: Token nằm trong data.access_token)
      localStorage.setItem('authToken', data.access_token);
      localStorage.setItem('userRole', 'customer');

      alert("Đăng nhập thành công!");

      // 3. Chuyển hướng (Vì đang mở tab mới nên có thể đóng tab hoặc redirect)
      // window.close(); // Nếu muốn đóng tab
      navigate('/');    // Nếu muốn về trang chủ

    } catch (error) {
      alert(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-container">

        {/* CỘT TRÁI */}
        <div className="auth-left">
          <div className="image-grid">
            <img src={imgPottery1} alt="Craft" className="img-main" />
            <img src={imgPottery2} alt="Craft Detail" className="img-sub" />

            {!isLogin && (
              <img src={imgPottery3} alt="Craft Extra" className="img-extra" />
            )
            }
          </div>

          <p className="quote">
            Một thế giới mới đang chờ bạn khám phá! Hãy đăng nhập để tiếp tục hành trình sáng tạo...
          </p>
        </div>

        {/*CỘT PHẢI*/}

        <div className="auth-right-wrapper">

          {/* 2. auth-switch */}
          <div className="auth-switch">
            <div className={`switch-slider ${isLogin ? 'left' : 'right'}`}>
            </div>

            <button
              className={`switch-btn ${isLogin ? 'active' : ''}`}
              onClick={() => setIsLogin(true)}
            >
              Đăng nhập
            </button>
            <button
              className={`switch-btn ${!isLogin ? 'active' : ''}`}
              onClick={() => setIsLogin(false)}
            >
              Đăng ký
            </button>
          </div>

          {/* 3. auth-right chứa Form */}
          <div className="auth-right">
            <div className="form-wrapper">
              <h2>{isLogin ? 'Đăng nhập' : 'Bắt đầu hành trình mới'}</h2>

              <form onSubmit={isLogin ? handleLogin : handleRegister}>

                {/* --- PHẦN 1: CÁC TRƯỜNG ĐĂNG KÝ (Ẩn/Hiện mượt mà) --- */}
                <div className={`collapse-section ${isLogin ? 'collapsed' : 'expanded'}`}>
                  <div className="form-group">
                    <label>Họ và tên</label>
                    {/* required={!isLogin} -> Chỉ bắt buộc nhập khi ĐANG LÀ form Đăng ký */}
                    <input type="text" name="name" value={formData.name} onChange={handleChange} required={!isLogin} />
                  </div>

                  <div className="form-group">
                    <label>Email</label>
                    <input type="email" name="email" value={formData.email} onChange={handleChange} required={!isLogin} />
                  </div>

                  <div className="form-group">
                    <label>Số điện thoại</label>
                    <input type="tel" name="phone_number" value={formData.phone_number} onChange={handleChange} required={!isLogin} />
                  </div>

                  <div className="form-group">
                    <label>Địa chỉ</label>
                    <input type="text" name="address" value={formData.address} onChange={handleChange} required={!isLogin} />
                  </div>
                </div>

                {/* --- PHẦN 2: CÁC TRƯỜNG CHUNG (Luôn hiện) --- */}
                <div className="form-group">
                  <label>{isLogin ? 'Email hoặc Tên đăng nhập' : 'Tên đăng nhập'}</label>
                  <input type="text" name="username" value={formData.username} onChange={handleChange} required />
                </div>


                <div className="form-group">

                  {/*Label bên trái - Link bên phải */}
                  <div className="label-row">
                    <label>Mật khẩu</label>
                    {isLogin && (
                      <a href="#" className="forgot-pass" onClick={(e) => e.preventDefault()}>
                        Quên mật khẩu?
                      </a>
                    )}
                  </div>

                  <input
                    type="password"
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    required
                  />
                </div>

                {/* CHECKBOX GHI NHỚ TÔI (Chỉ hiện khi Login) --- */}
                {isLogin && (
                  <div className="form-options remember-me">
                    <label>
                      <input type="checkbox" /> Ghi nhớ tôi
                    </label>
                  </div>
                )}

                {/* --- PHẦN 3: XÁC NHẬN MẬT KHẨU (Cũng cần ẩn/hiện mượt mà) --- */}
                <div className={`collapse-section ${isLogin ? 'collapsed' : 'expanded'}`}>
                  <div className="form-group">
                    <label>Xác nhận mật khẩu</label>
                    <input type="password" name="confirmPassword" value={formData.confirmPassword} onChange={handleChange} required={!isLogin} />
                  </div>
                </div>

                {/* CHECKBOX ĐIỀU KHOẢN */}
                <div className={`collapse-section ${isLogin ? 'collapsed' : 'expanded'}`}>
                  <div className="form-options terms-checkbox">
                    <label>
                      <input
                        type="checkbox"
                        checked={agreeTerms}
                        onChange={(e) => setAgreeTerms(e.target.checked)}
                      />
                      <span>
                        Tôi đồng ý với{' '}
                        <a href="#" onClick={(e) => e.preventDefault()}>Điều khoản dịch vụ</a>
                        {' '}và{' '}
                        <a href="#" onClick={(e) => e.preventDefault()}>Chính sách bảo mật</a>
                      </span>
                    </label>
                  </div>
                </div>

                {/* --- BUTTON & SOCIAL --- */}
                <button type="submit" className="btn-submit" disabled={isLoading}>
                  {isLoading ? 'Đang xử lý...' : (isLogin ? 'Đăng nhập' : 'Đăng ký')}
                </button>

                {/* Phần Social Login cũng cần ẩn mượt mà khi chuyển sang Đăng ký */}
                <div className={`collapse-section social-section ${isLogin ? 'expanded' : 'collapsed'}`}>
                  <div className="social-login">
                    <span>Hoặc đăng nhập với</span>
                    <div className="icons">
                      <button type="button" className="icon-btn google">G</button>
                      <button type="button" className="icon-btn facebook">F</button>
                    </div>
                  </div>
                </div>

              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AuthPage;