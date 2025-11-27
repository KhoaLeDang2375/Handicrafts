import { Routes, Route, useLocation } from 'react-router-dom';

// 1. Import các component layout
import Navbar from './components/layout/Navbar';
import Footer from './components/layout/Footer';

// 2. Import các trang
import HomePage from './pages/HomePage/HomePage';
import ProductPage from './pages/ProductPage/ProductPage'; 
import AuthPage from './pages/AuthPage/AuthPage';
import ProductDetailPage from './pages/ProductDetailPage/ProductDetailPage';

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

        </Routes>
      </main>

      {/* Chỉ hiện Footer nếu KHÔNG PHẢI trang login */}
      {!isLoginPage && <Footer />}
      
    </div>
  );
}

export default App;