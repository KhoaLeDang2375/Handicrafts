import { Routes, Route, useLocation } from 'react-router-dom';

// 1. Import các component layout
import Navbar from './components/layout/Navbar';
import Footer from './components/layout/Footer';

// 2. Import các trang
import HomePage from './pages/HomePage/HomePage';
import ProductPage from './pages/ProductPage/ProductPage'; 
import AuthPage from './pages/AuthPage/AuthPage';
import ProductDetailPage from './pages/ProductDetailPage/ProductDetailPage';
import CartPage from './pages/CartPage/CartPage';
import CheckoutPage from './pages/CheckoutPage/CheckoutPage';
import ProfilePage from './pages/ProfilePage/ProfilePage'; 
import AboutPage from './pages/AboutPage/AboutPage';
import ContactPage from './pages/ContactPage/ContactPage';
import BlogPage from './pages/Blog/BlogPage';

import AdminBlogManager from './pages/Admin/AdminBlogManager';

function App() {
  const location = useLocation();

  const isLoginPage = location.pathname === '/login';

  return (
    <div className="App">
      {/* Chỉ hiện Navbar nếu KHÔNG PHẢI trang login */}
      {!isLoginPage && <Navbar />}

      <main>
        <Routes>
          
          <Route path="/" element={<HomePage />} />
          
          <Route path="/san-pham" element={<ProductPage />} />

          <Route path="/login" element={<AuthPage />} />

          <Route path="/san-pham/:id" element={<ProductDetailPage />} />

          <Route path="/ve-chung-toi" element={<AboutPage />} />

          <Route path="/cart" element={<CartPage />} />

          <Route path="/thanh-toan" element={<CheckoutPage />} />

          <Route path="/my-profile" element={<ProfilePage />} />

          <Route path="/lien-he" element={<ContactPage />} />

          <Route path="/blog" element={<BlogPage />} />

          <Route path="/admin/blogs" element={<AdminBlogManager />} />

        </Routes>
      </main>

      {/* Chỉ hiện Footer nếu KHÔNG PHẢI trang login */}
      {!isLoginPage && <Footer />}
      
    </div>
  );
}

export default App;