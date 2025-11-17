import { useState, useEffect } from 'react';
import './CategoryNav.scss';

const CategoryNav = () => {
  // 1. Tạo state để theo dõi trạng thái "dính"
  const [isSticky, setIsSticky] = useState(false);

  // 2. Dùng useEffect để lắng nghe sự kiện cuộn (scroll)
  useEffect(() => {
    const handleScroll = () => {
      // Ngay khi người dùng cuộn trang (dù chỉ 1px) sẽ kích hoạt trạng thái "dính"
      setIsSticky(window.scrollY > 0);
    };

    // Thêm listener khi component được mount
    window.addEventListener('scroll', handleScroll);

    // Gỡ listener khi component bị unmount
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []); // [] đảm bảo effect này chỉ chạy 1 lần

  // 3. Gán class 'is-sticky' nếu state là true
  return (
    <nav className={isSticky ? 'category-nav is-sticky' : 'category-nav'}>
      <button className="category-btn active">Tất cả sản phẩm</button>
      <button className="category-btn">Nội thất</button>
      <button className="category-btn">Túi xách</button>
      <button className="category-btn">Thảm</button>
      <button className="category-btn">Trang trí nhà cửa</button>
    </nav>
  );
};

export default CategoryNav;