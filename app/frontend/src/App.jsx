import { Routes, Route, useLocation } from 'react-router-dom';

// 1. Import các component layout
import Navbar from './components/layout/Navbar';
import Footer from './components/layout/Footer';

// 2. Import các trang
import HomePage from './pages/HomePage/HomePage';
import ProductPage from './pages/ProductPage/ProductPage'; 
import AuthPage from './pages/AuthPage/AuthPage';

function App() {
  const location = useLocation();

  const isLoginPage = location.pathname === '/login';

  return (
    <div className="App">
      {/* Navbar sẽ luôn ở trên cùng */}
      <Navbar />

      <main>
        <Routes>
          
          <Route path="/" element={<HomePage />} />
          
          <Route path="/san-pham" element={<ProductPage />} />

          <Route path="/login" element={<AuthPage />} />

        </Routes>
      </main>

      {/* 6. Chỉ hiện Footer nếu KHÔNG PHẢI trang login */}
      {!isLoginPage && <Footer />}
      
    </div>
  );
}

export default App;