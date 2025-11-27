// import React from 'react';
import { useState, useEffect } from 'react';
import { Link, NavLink } from 'react-router-dom';
import './Navbar.scss';
import Logo from '../../assets/images/Aura.png';

// Ảnh avatar giả lập
import Avatar from "../../assets/images/avatar.png";
// const Avatar_URL = "https://i.pravatar.cc/150?img=3";

const Navbar = () => {
  // State để lưu trạng thái đăng nhập
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  // Kiểm tra token khi component được load
  useEffect(() => {
    // Lấy token từ localStorage (nơi bạn đã lưu khi login thành công)
    const token = localStorage.getItem('authToken');
    // Nếu có token -> set isLoggedIn = true. Ngược lại = false.
    // (Dấu !! giúp chuyển đổi giá trị truthy/falsy thành boolean true/false)
    setIsLoggedIn(!!token);
  }, []);

  return (
    <nav className="navbar">

      <div className="navbar__container">

        {/* 1. Logo */}
        <div className="navbar__logo">
          <div className="img__logo">
            <img src={Logo} alt="Aura Store Logo" />
          </div>
        </div>

        <ul className="navbar__links">
          <li><NavLink to="/">TRANG CHỦ</NavLink></li>
          <li><NavLink to="/san-pham">SẢN PHẨM</NavLink></li>
          <li><NavLink to="/ve-chung-toi">VỀ CHÚNG TÔI</NavLink></li>
          <li><NavLink to="/blog">BLOG</NavLink></li>
          <li><NavLink to="/lien-he">LIÊN HỆ</NavLink></li>
        </ul>

        <div className="navbar__actions">
          <div className="navbar__search">
            <input type="text" placeholder="Tìm kiếm" />
            <button className="search-icon">
              {/* Icon kính lúp */}
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.099zm-5.442-4.14a5.5 5.5 0 1 1 0 11 5.5 5.5 0 0 1 0-11z" />
              </svg>
            </button>
          </div>

          {isLoggedIn ? (
            // --- GIAO DIỆN KHI ĐÃ ĐĂNG NHẬP ---
            <div className="navbar__user-area">

              {/* Icon Giỏ hàng */}
              <Link to="/cart" className="navbar__action-icon cart-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <circle cx="9" cy="21" r="1"></circle>
                  <circle cx="20" cy="21" r="1"></circle>
                  <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
                </svg>
              </Link>

              {/* Avatar người dùng */}
              <Link to="/profile" className="navbar__avatar">
                <img src={Avatar} alt="User Avatar" />
              </Link>
            </div>

          ) : (
            // --- GIAO DIỆN KHI CHƯA ĐĂNG NHẬP ---
            <Link
              to="/login"
              className="btn btn--primary"
              target="_blank"
              rel="noopener noreferrer"
            >
              Đăng nhập
            </Link>
          )}

        </div>
      </div>
    </nav>
  );
};

export default Navbar;

