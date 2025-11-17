// import React from 'react';
import { NavLink } from 'react-router-dom';
import './Navbar.scss';
import Logo from '../../assets/images/Aura.png';

const Navbar = () => {
    return (
        <nav className="navbar">
            {/* THÊM DIV CONTAINER NÀY */}
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
                            {/* Đây là icon kính lúp, bạn có thể thay bằng React Icons */}
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                                <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.099zm-5.442-4.14a5.5 5.5 0 1 1 0 11 5.5 5.5 0 0 1 0-11z" />
                            </svg>
                        </button>
                    </div>
                    <button className="btn btn--primary">Đăng nhập</button>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;