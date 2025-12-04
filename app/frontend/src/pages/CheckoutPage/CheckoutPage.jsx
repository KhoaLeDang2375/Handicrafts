import { useState, useEffect } from 'react';
import { useLocation, useNavigate, Link } from 'react-router-dom';
import { apiCall } from '../../services/api';
import './CheckoutPage.scss';

import { FiArrowLeft, FiMapPin, FiTruck, FiCreditCard, FiDollarSign, FiLock } from 'react-icons/fi';
import Logo from '../../assets/images/Aura.png';

const SHIPPING_RATES = { 'GHTK': 30000, 'GNN': 45000 };

const CheckoutPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [currentUser, setCurrentUser] = useState(null);

  // 1. Lấy dữ liệu từ state (Hỗ trợ cả 2 trường hợp)
  const { productToBuy, checkoutItems } = location.state || {};

  // 2. CHUẨN HÓA DỮ LIỆU VỀ MỘT MẢNG DUY NHẤT
  const [orderItems, setOrderItems] = useState([]);

  useEffect(() => {
    if (checkoutItems && checkoutItems.length > 0) {
      // Trường hợp 1: Từ Giỏ hàng (đã là mảng)
      setOrderItems(checkoutItems);
    } else if (productToBuy) {
      // Trường hợp 2: Mua ngay (biến thành mảng 1 phần tử)
      setOrderItems([{
        ...productToBuy,
        product_quantity: productToBuy.quantity, // Mua ngay dùng field 'quantity', cart dùng 'product_quantity'
        product_name: productToBuy.name,         // Mua ngay dùng 'name', cart dùng 'product_name'
      }]);
    } else {
      navigate('/');
    }
  }, [productToBuy, checkoutItems, navigate]);


  // Load thông tin User từ LocalStorage khi vào trang
  useEffect(() => {
    const userStored = localStorage.getItem('currentUser');
    
    if (userStored) {
      // Lưu thẳng vào state currentUser để hiển thị lên giao diện
      setCurrentUser(JSON.parse(userStored)); 
    } else {
      // Nếu chưa đăng nhập thì đuổi về trang login
      alert("Vui lòng đăng nhập để thanh toán!");
        navigate('/login');
    }
  }, []);

  const [shippingMethod, setShippingMethod] = useState('GHTK'); // Mặc định GHTK
  const [paymentMethod, setPaymentMethod] = useState('COD');   // Mặc định COD

  // --- 3. TÍNH TOÁN TỔNG TIỀN (Dựa trên mảng orderItems) ---
  const subTotal = orderItems.reduce((sum, item) => {
    // Giá * Số lượng
    return sum + (item.price * (item.product_quantity || item.quantity));
  }, 0);

  const isFreeShip = subTotal >= 500000;
  const baseShippingFee = SHIPPING_RATES[shippingMethod] || 0;
  const shippingFee = isFreeShip ? 0 : baseShippingFee;
  const total = subTotal + shippingFee;

  // --- 4. Gửi dữ liệu đặt hàng ---
  useEffect(() => {
    const userStored = localStorage.getItem('currentUser');
    if (userStored) {
      setCurrentUser(JSON.parse(userStored));
    }
  }, []);

  // --- HÀM ĐẶT HÀNG MỚI ---
  const handlePlaceOrder = async () => {
    const token = localStorage.getItem('authToken');
    if (!token) {
        alert("Vui lòng đăng nhập lại.");
        return;
    }

    // 1. Validate thông tin User
    if (!currentUser || !currentUser.address || !currentUser.phone) {
      alert("Hồ sơ thiếu Địa chỉ hoặc SĐT. Vui lòng cập nhật trước!");
      // navigate('/profile'); 
      return;
    }

    // 2. Xác định: Đây là "Mua ngay" hay "Thanh toán giỏ hàng"?
    // (Dựa vào state fromCart truyền từ trang trước)
    const isBuyNow = !location.state?.fromCart; 

    // 3. Chuẩn bị dữ liệu CHUNG (Cả 2 trường hợp đều cần)
    const commonPayload = {
      access_token: token,
      customer_info: {
        name: currentUser.name || currentUser.fullname,
        phone: currentUser.phone,
        email: currentUser.email,
        address: currentUser.address
      },
      shipment: shippingMethod,
      payment_method: paymentMethod,
      total_amount: total
    };

    let payload = {};
    let endpoint = "";

    // 4. Cấu hình Payload và Endpoint riêng biệt
    if (isBuyNow) {
        // --- TRƯỜNG HỢP MUA NGAY ---
        endpoint = "/orders/buy-now";
        
        // Backend 'OrderCheckoutOne' yêu cầu field 'item' là 1 object đơn lẻ
        payload = {
            ...commonPayload,
            item: {
                productvariant_id: orderItems[0].variant_id || orderItems[0].productvariant_id,
                product_quantity: orderItems[0].product_quantity || orderItems[0].quantity
            }
        };
    } else {
        // --- TRƯỜNG HỢP GIỎ HÀNG ---
        endpoint = "/orders/checkout";
        
        // Backend 'OrderCheckout' yêu cầu field 'cart_items' là 1 mảng
        payload = {
            ...commonPayload,
            cart_items: orderItems.map(item => ({
                productvariant_id: item.variant_id || item.productvariant_id,
                product_quantity: item.product_quantity || item.quantity
            }))
        };
    }

    console.log(`Đang gọi ${endpoint} với dữ liệu:`, payload);

    try {
      // 5. Gọi API (Endpoint động)
      const response = await apiCall(endpoint, {
        method: 'POST',
        body: JSON.stringify(payload)
      });
      
      const data = await response.json();

      if (response.ok) {
        alert(`Đặt hàng thành công! Mã đơn: #${data.order_id}`);
        navigate('/'); // Hoặc chuyển sang trang lịch sử đơn hàng
      } else {
        alert(`Lỗi: ${data.detail || 'Đặt hàng thất bại'}`);
      }
    } catch (error) {
      console.error("Lỗi connection:", error);
      alert("Không thể kết nối đến server.");
    }
  };

  if (orderItems.length === 0) return null;

  const backLink = location.state?.fromCart
    ? "/cart"
    : `/san-pham/${orderItems[0].product_id}`;

  return (
    <div className="checkout-page">

      <div className="checkout-container">
        <div className="checkout-header">
          <Link to={backLink} className="back-link">
            <FiArrowLeft size={18} style={{ marginRight: '5px', verticalAlign: 'middle' }} />
            {location.state?.fromCart ? "Quay lại giỏ hàng" : "Quay lại sản phẩm"}
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

              {currentUser ? (
                <div className="default-address-card">
                  <p className="name"><strong>{currentUser.name}</strong></p>
                  <p className="phone">Số điện thoại: {currentUser.phone || "Chưa có SĐT"}</p>
                  <p className="address">Địa chỉ: {currentUser.address || "Chưa cập nhật địa chỉ"}</p>
                  <p className="email">Email: {currentUser.email}</p>

                  <Link to="/profile" style={{ fontSize: '0.9rem', color: '#d49058', marginTop: '0.5rem', display: 'inline-block' }}>
                    Thay đổi thông tin
                  </Link>
                </div>
              ) : (
                <p>Vui lòng đăng nhập để tải địa chỉ.</p>
              )}

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

                  <div className="method-price-group">
                    {isFreeShip && <span className="original-fee">30.000₫</span>}
                    <span className={`method-price ${isFreeShip ? 'free' : ''}`}>
                      {isFreeShip ? 'Miễn phí' : '30.000₫'}
                    </span>
                  </div>
                </label>

                <label className={`radio-card ${shippingMethod === 'GNN' ? 'active' : ''}`}>
                  <input type="radio" name="shipping" value="GNN" checked={shippingMethod === 'GNN'} onChange={(e) => setShippingMethod(e.target.value)} />
                  <div className="radio-content">
                    <span className="method-name">Giao Hàng Nhanh (GNN)</span>
                    <span className="method-desc">Giao trong 1-2 ngày</span>
                  </div>

                  <div className="method-price-group">
                    {isFreeShip && <span className="original-fee">45.000₫</span>}
                    <span className={`method-price ${isFreeShip ? 'free' : ''}`}>
                      {isFreeShip ? 'Miễn phí' : '45.000₫'}
                    </span>
                  </div>
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
                  <span className="icon" style={{ color: '#d82d8b', fontWeight: 'bold' }}>MOMO</span>
                </label>
              </div>
            </div>

          </div>

          {/* --- CỘT PHẢI: ĐƠN HÀNG --- */}
          <div className="checkout-right">
            <div className="order-summary-box">
              <h3>Đơn hàng của bạn ({orderItems.length} sản phẩm)</h3>

              <div className="order-items">
                {/* DÙNG VÒNG LẶP ĐỂ HIỂN THỊ DANH SÁCH */}
                {orderItems.map((item, index) => (
                  <div key={index} className="order-item">
                    <div className="item-image">
                      {/* Xử lý ảnh: item.image (cart) hoặc item.image (buy now) */}
                      <img src={item.image || Logo} alt={item.product_name} />
                      <span className="item-qty">{item.product_quantity || item.quantity}</span>
                    </div>
                    <div className="item-details">
                      {/* Xử lý tên: item.product_name (cart) hoặc item.name (buy now) */}
                      <h4>{item.product_name || item.name}</h4>
                      <p>{item.color} {item.size ? `/ ${item.size}` : ''}</p>
                    </div>
                    <div className="item-price">
                      {(item.price * (item.product_quantity || item.quantity)).toLocaleString('vi-VN')}₫
                    </div>
                  </div>
                ))}
              </div>

              <div className="summary-row">
                <span>Tạm tính</span>
                <span>{subTotal.toLocaleString('vi-VN')}₫</span>
              </div>
              <div className="summary-row">
                <span>Phí vận chuyển ({shippingMethod})</span>
                {isFreeShip ? <span style={{ color: '#2ecc71' }}>Miễn phí</span> : <span>{baseShippingFee.toLocaleString('vi-VN')}₫</span>}
              </div>
              <div className="summary-divider"></div>
              <div className="summary-total">
                <span>Tổng cộng</span>
                <span className="total-price">{total.toLocaleString('vi-VN')}₫</span>
              </div>

              <button className="btn-place-order" onClick={handlePlaceOrder}>Đặt hàng</button>

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