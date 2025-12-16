// import React from 'react';
import { useState, useEffect } from 'react';
import { Link, NavLink, useNavigate } from 'react-router-dom';
import { FaSearch } from "react-icons/fa";
import './Navbar.scss';
import Logo from '../../assets/images/Aura.png';

// Ảnh avatar giả lập
import Avatar from "../../assets/images/avatar.png";
// const Avatar_URL = "https://i.pravatar.cc/150?img=3";

const Navbar = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userInfo, setUserInfo] = useState({ name: 'Khách hàng', email: 'email' }); // State lưu thông tin user
  // State lưu role
  const [userRole, setUserRole] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('authToken');
    setIsLoggedIn(!!token);

    // Lấy Role từ localStorage
    const role = localStorage.getItem('userRole');
    setUserRole(role);

    // Lấy thông tin user từ localStorage 
    const userStored = localStorage.getItem('currentUser');
    if (userStored) {
      const user = JSON.parse(userStored);
      setUserInfo({
        name: user.name || "Khách hàng",
        email: user.email || "email"
      });
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userRole');
    localStorage.removeItem('currentUser'); // Xóa cả thông tin user
    setIsLoggedIn(false);
    alert("Bạn đã đăng xuất thành công!");
    navigate('/login');
  };

  return (
    <nav className="navbar">

      <div className="navbar__container">

        {/* 1. Logo */}
        <div className="navbar__logo">
          <div className="img__logo">
            <img src={Logo} alt="Aura Store Logo" />
          </div>
        </div>

        {/* Logic điều hướng dựa trên Role */}
        <ul className="navbar__links">
          {userRole === 'employee' ? (
            // --- MENU DÀNH CHO NHÂN VIÊN ---
            <>
              <li><NavLink to="/admin/blogs">BLOG NHÂN VIÊN</NavLink></li>
              <li><NavLink to="/blog">BLOG CÔNG KHAI</NavLink></li>
              <li><NavLink to="/dashboard">DASHBOARD</NavLink></li>
              <li><NavLink to="/customers">DANH SÁCH KHÁCH HÀNG</NavLink></li>
              {/* Bạn có thể thêm các menu quản lý khác ở đây */}
            </>
          ) : (
            // --- MENU DÀNH CHO KHÁCH HÀNG (Mặc định) ---
            <>
              <li><NavLink to="/">TRANG CHỦ</NavLink></li>
              <li><NavLink to="/san-pham">SẢN PHẨM</NavLink></li>
              <li><NavLink to="/ve-chung-toi">VỀ CHÚNG TÔI</NavLink></li>
              <li><NavLink to="/blog">BLOG</NavLink></li>
              <li><NavLink to="/lien-he">LIÊN HỆ</NavLink></li>
            </>
          )}
        </ul>

        <div className="navbar__actions">
          <div className="navbar__search">
            <input type="text" placeholder="Tìm kiếm" />
            <button className="search-icon">
              {/* Icon kính lúp */}
              <FaSearch />
            </button>
          </div>

          {isLoggedIn ? (
            // --- GIAO DIỆN KHI ĐÃ ĐĂNG NHẬP ---
            <div className="navbar__user-area">

              {/* Ẩn giỏ hàng nếu là Employee */}
              {userRole !== 'employee' && (
                <Link to="/cart" className="navbar__action-icon cart-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <circle cx="9" cy="21" r="1"></circle>
                    <circle cx="20" cy="21" r="1"></circle>
                    <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
                  </svg>
                </Link>
              )}

              <div className="user-dropdown-wrapper">
                <div className="navbar__avatar">
                  <img src={Avatar} alt="User" />
                </div>

                {/* Nội dung Menu */}
                <div className="dropdown-menu">
                  {/* Header: Tên và Email */}
                  <div className="dropdown-header">
                    <p className="user-name">{userInfo.name}</p>
                    <p className="user-email">{userInfo.email}</p>
                    <p style={{ fontSize: '0.9rem', color: '#00c4cc' }}>
                      {userRole === 'employee' ? 'Nhân viên' : 'Khách hàng'}
                    </p>
                  </div>

                  <div className="dropdown-divider"></div>

                  {/* Các Link: Profile, Setting */}
                  <Link to="/my-profile" className="dropdown-item">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
                    Xem profile
                  </Link>

                  <Link to="/settings" className="dropdown-item">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>
                    Cài đặt
                  </Link>

                  <div className="dropdown-divider"></div>

                  {/* Nút Đăng xuất */}
                  <button onClick={handleLogout} className="dropdown-item logout-btn">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>
                    Đăng xuất
                  </button>
                </div>
              </div>
              {/* ------------------------------------------- */}
            </div>
          ) : (
            <Link to="/login" className="btn btn--primary" target="_blank" rel="noopener noreferrer">Đăng nhập</Link>
          )}

        </div>
      </div>
    </nav>
  );
};

export default Navbar;

