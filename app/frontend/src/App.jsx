import { Routes, Route } from 'react-router-dom';

// 1. Import các component layout
import Navbar from './components/layout/Navbar';
import Footer from './components/layout/Footer';

// 2. Import các trang
import HomePage from './pages/HomePage/HomePage';
import ProductPage from './pages/ProductPage/ProductPage'; 


function App() {
  return (
    <div className="App">
      {/* Navbar sẽ luôn ở trên cùng */}
      <Navbar />

      <main>
        <Routes>
          
          <Route path="/" element={<HomePage />} />
          
          <Route path="/san-pham" element={<ProductPage />} />

        </Routes>
      </main>

      {/* Footer sẽ luôn ở dưới cùng */}
      <Footer />
    </div>
  );
}

export default App;