// src/pages/ProductPage/CategoryNav.jsx
import { useState, useEffect } from 'react';
import './CategoryNav.scss';

// Nhận props từ cha
const CategoryNav = ({ categories, activeCategory, onSelectCategory }) => {
  const [isSticky, setIsSticky] = useState(false);

  useEffect(() => {
    const handleScroll = () => setIsSticky(window.scrollY > 0);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <nav className={isSticky ? 'category-nav is-sticky' : 'category-nav'}>
      {categories.map((cat) => (
        <button
          key={cat.id}
          // Nếu id của nút này trùng với activeCategory từ cha -> Thêm class active
          className={`category-btn ${activeCategory === cat.id ? 'active' : ''}`}
          
          // Khi click -> Gọi hàm của cha để đổi state
          onClick={() => onSelectCategory(cat.id)}
        >
          {cat.label}
        </button>
      ))}
    </nav>
  );
};

export default CategoryNav;
