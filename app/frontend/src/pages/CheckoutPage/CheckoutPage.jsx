import { useState, useEffect } from 'react';
import { useLocation, useNavigate, Link } from 'react-router-dom';
import './CheckoutPage.scss';

import { 
  FiArrowLeft,    
  FiMapPin,      
  FiTruck,     
  FiCreditCard, 
  FiDollarSign,
  FiLock         
} from 'react-icons/fi';
import Logo from '../../assets/images/Aura.png';
const SHIPPING_RATES = {
  'GHTK': 30000,
  'GNN': 45000
};

const CheckoutPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  
  // 1. Lấy dữ liệu sản phẩm được truyền từ trang trước (qua state của navigate)
  const { productToBuy } = location.state || {};

  // Nếu không có sản phẩm nào (người dùng truy cập trực tiếp link), quay về trang chủ
  useEffect(() => {
    if (!productToBuy) {
      navigate('/');
    }
  }, [productToBuy, navigate]);

  // 2. State cho Form thông tin
  const [formData, setFormData] = useState({
    fullName: '',
    phone: '',
    email: '',
    address: '',
    city: '',
    district: '',
    ward: '',
    note: ''
  });

  // Tự động điền thông tin nếu đã đăng nhập (Lấy từ localStorage)
  useEffect(() => {
    const userStored = localStorage.getItem('currentUser');
    if (userStored) {
      const user = JSON.parse(userStored);
      setFormData(prev => ({
        ...prev,
        fullName: user.name || '',
        email: user.email || '',
        phone: user.phone || '', 
        address: user.address || ''
      }));
    }
  }, []);

  const [shippingMethod, setShippingMethod] = useState('GHTK'); // Mặc định GHTK
  const [paymentMethod, setPaymentMethod] = useState('COD');   // Mặc định COD

  // Tính toán tiền
  const itemPrice = productToBuy ? productToBuy.price : 0;
  const quantity = productToBuy ? productToBuy.quantity : 1;
  
  // 1. Tính tổng tiền hàng
  const subTotal = itemPrice * quantity;

  // 2. Kiểm tra điều kiện Freeship
  const isFreeShip = subTotal >= 500000;

  // 3. Lấy giá ship gốc dựa trên phương thức đang chọn
  const baseShippingFee = SHIPPING_RATES[shippingMethod] || 0;

  // 4. Tính phí ship cuối cùng (Nếu Free thì = 0, ngược lại lấy giá gốc)
  const finalShippingFee = isFreeShip ? 0 : baseShippingFee;

  // 5. Tổng thanh toán
  const total = subTotal + finalShippingFee;

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handlePlaceOrder = () => {
    // Logic gọi API tạo đơn hàng sẽ viết ở đây sau
    alert("Đang xử lý đặt hàng...");
    console.log({
      customer: formData,
      items: [productToBuy],
      shipping: shippingMethod,
      payment: paymentMethod,
      total: total
    });
  };

  if (!productToBuy) return null;


  return (
    <div className="checkout-page">
      
      <div className="checkout-container">
        <div className="checkout-header">
            <Link to={`/san-pham/${productToBuy.product_id}`} className="back-link">
                <FiArrowLeft size={18} style={{ marginRight: '5px', verticalAlign: 'middle' }} />
                Quay lại sản phẩm
            </Link>
            <h1>Thanh toán</h1>
        </div>

        <div className="checkout-layout">
          
          {/* --- CỘT TRÁI: THÔNG TIN --- */}
          <div className="checkout-left">
            
            {/* 1. Thông tin giao hàng */}
            <div className="checkout-section">
              <h3>
                <FiMapPin style={{ marginRight: '8px', color: '#d49058' }} />
                Thông tin giao hàng
              </h3>
              <div className="form-row">
                <div className="form-group half">
                  <label>Họ và tên *</label>
                  <input type="text" name="fullName" value={formData.fullName} onChange={handleInputChange} placeholder="Nguyễn Văn A" />
                </div>
                <div className="form-group half">
                  <label>Số điện thoại *</label>
                  <input type="text" name="phone" value={formData.phone} onChange={handleInputChange} placeholder="09xxxxxxx" />
                </div>
              </div>
              
              <div className="form-group">
                <label>Email *</label>
                <input type="email" name="email" value={formData.email} onChange={handleInputChange} placeholder="email@example.com" />
              </div>

              {/* (Phần Tỉnh/Huyện/Xã có thể làm dropdown sau, tạm thời dùng input text) */}
              <div className="form-group">
                <label>Địa chỉ cụ thể *</label>
                <input type="text" name="address" value={formData.address} onChange={handleInputChange} placeholder="Số nhà, tên đường..." />
              </div>
              
              <div className="form-group">
                <label>Ghi chú (tùy chọn)</label>
                <textarea name="note" rows="2" value={formData.note} onChange={handleInputChange} placeholder="Ghi chú về đơn hàng..."></textarea>
              </div>
            </div>

            {/* 2. Phương thức vận chuyển */}
            <div className="checkout-section">
              <h3>
                <FiTruck style={{ marginRight: '8px', color: '#d49058' }} />
                Phương thức vận chuyển
              </h3>
              <div className="radio-group">
                <label className={`radio-card ${shippingMethod === 'GHTK' ? 'active' : ''}`}>
                  <input type="radio" name="shipping" value="GHTK" checked={shippingMethod === 'GHTK'} onChange={(e) => setShippingMethod(e.target.value)} />
                  <div className="radio-content">
                    <span className="method-name">Giao Hàng Tiết Kiệm (GHTK)</span>
                    <span className="method-desc">Giao trong 3-5 ngày</span>
                  </div>
                  <span className="method-price">30.000₫</span>
                </label>

                <label className={`radio-card ${shippingMethod === 'GNN' ? 'active' : ''}`}>
                  <input type="radio" name="shipping" value="GNN" checked={shippingMethod === 'GNN'} onChange={(e) => setShippingMethod(e.target.value)} />
                  <div className="radio-content">
                    <span className="method-name">Giao Hàng Nhanh (GNN)</span>
                    <span className="method-desc">Giao trong 1-2 ngày</span>
                  </div>
                  <span className="method-price">45.000₫</span>
                </label>
              </div>
            </div>

            {/* 3. Phương thức thanh toán */}
            <div className="checkout-section">
              <h3>
                <FiCreditCard style={{ marginRight: '8px', color: '#d49058' }} />
                Phương thức thanh toán
              </h3>
              <div className="radio-group">
                <label className={`radio-card ${paymentMethod === 'COD' ? 'active' : ''}`}>
                  <input type="radio" name="payment" value="COD" checked={paymentMethod === 'COD'} onChange={(e) => setPaymentMethod(e.target.value)} />
                  <div className="radio-content">
                    <span className="method-name">Thanh toán khi nhận hàng (COD)</span>
                    <span className="method-desc">Thanh toán bằng tiền mặt</span>
                  </div>
                  <FiDollarSign size={24} color="#2ecc71" />
                </label>

                <label className={`radio-card ${paymentMethod === 'MOMO' ? 'active' : ''}`}>
                  <input type="radio" name="payment" value="MOMO" checked={paymentMethod === 'MOMO'} onChange={(e) => setPaymentMethod(e.target.value)} />
                  <div className="radio-content">
                    <span className="method-name">Ví MoMo</span>
                    <span className="method-desc">Thanh toán qua ví điện tử</span>
                  </div>
                  <span className="icon" style={{color: '#d82d8b', fontWeight: 'bold'}}>MOMO</span>
                </label>
              </div>
            </div>

          </div>

          {/* --- CỘT PHẢI: ĐƠN HÀNG --- */}
          <div className="checkout-right">
            <div className="order-summary-box">
              <h3>Đơn hàng của bạn</h3>
              
              <div className="order-items">
                <div className="order-item">
                    <div className="item-image">
                        <img src={productToBuy.image || Logo} alt={productToBuy.name} />
                        <span className="item-qty">{productToBuy.quantity}</span>
                    </div>
                    <div className="item-details">
                        <h4>{productToBuy.name}</h4>
                        <p>{productToBuy.color} / {productToBuy.size}</p>
                    </div>
                    <div className="item-price">
                        {(itemPrice * quantity).toLocaleString('vi-VN')}₫
                    </div>
                </div>
              </div>

              <div className="summary-row">
                <span>Tạm tính</span>
                <span>{subTotal.toLocaleString('vi-VN')}₫</span>
              </div>
              <div className="summary-row">
                <span>Phí vận chuyển ({shippingMethod})</span>
                <span>{shippingFee.toLocaleString('vi-VN')}₫</span>
              </div>
              
              <div className="summary-divider"></div>
              
              <div className="summary-total">
                <span>Tổng cộng</span>
                <span className="total-price">{total.toLocaleString('vi-VN')}₫</span>
              </div>

              <button className="btn-place-order" onClick={handlePlaceOrder}>
                Đặt hàng
              </button>
              
              <div className="security-note">
                <FiLock size={16} style={{ marginRight: '5px' }} />
                Thông tin thanh toán được bảo mật an toàn
              </div>
            </div>
          </div>

        </div>
      </div>
     
    </div>
  );
};

export default CheckoutPage;