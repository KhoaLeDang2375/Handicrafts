import { useState, useEffect } from 'react';
import { useLocation, useNavigate, Link } from 'react-router-dom';
import { checkoutCart, buyNow } from '../../services/orderApi';
import './CheckoutPage.scss';

import { FiArrowLeft, FiMapPin, FiTruck, FiCreditCard, FiDollarSign, FiLock } from 'react-icons/fi';
import Logo from '../../assets/images/Aura.png';

const SHIPPING_RATES = { 'GHTK': 30000, 'GNN': 45000 };

const CheckoutPage = () => {

  const location = useLocation();
  const navigate = useNavigate();
  const [currentUser, setCurrentUser] = useState(null);

  // Form giao hàng riêng (nếu chọn giao địa chỉ khác)
  const [shippingForm, setShippingForm] = useState({ name: '', phone: '', address: '' });
  const [isCustomShipping, setIsCustomShipping] = useState(false);

  const [shippingMethod, setShippingMethod] = useState('GHTK');
  const [paymentMethod, setPaymentMethod] = useState('COD');
  const [orderItems, setOrderItems] = useState([]);

  // Lấy dữ liệu state truyền sang
  const { productToBuy, checkoutItems } = location.state || {};

  // 1. Load User & Chuẩn hóa dữ liệu ngay khi vào trang
  useEffect(() => {
    // --- Xử lý User ---
    const userStored = localStorage.getItem('currentUser');
    if (userStored) {
      setCurrentUser(JSON.parse(userStored));
    } else {
      alert("Vui lòng đăng nhập để thanh toán!");
      navigate('/login');
      return;
    }

    // --- Xử lý Items ---
    if (checkoutItems && checkoutItems.length > 0) {
      // Từ Giỏ hàng
      setOrderItems(checkoutItems);
    } else if (productToBuy) {
      // Mua ngay -> Chuyển thành mảng 1 phần tử
      setOrderItems([{
        ...productToBuy,
        product_quantity: productToBuy.quantity,
        product_name: productToBuy.name,
      }]);
    } else {
      navigate('/'); // Không có dữ liệu thì về trang chủ
    }
  }, [productToBuy, checkoutItems, navigate]);

  const handleShippingChange = (e) => {
    const { name, value } = e.target;
    setShippingForm(prev => ({ ...prev, [name]: value }));
  };

  // 2. Tính toán tiền
  const subTotal = orderItems.reduce((sum, item) => {
    return sum + (item.price * (item.product_quantity || item.quantity));
  }, 0);

  const isFreeShip = subTotal >= 500000;
  const baseShippingFee = SHIPPING_RATES[shippingMethod] || 0;
  const shippingFee = isFreeShip ? 0 : baseShippingFee;
  const total = subTotal + shippingFee;

  // --- 3. XỬ LÝ ĐẶT HÀNG (ĐÃ TỐI ƯU) ---
  const handlePlaceOrder = async () => {
    const token = localStorage.getItem('authToken');
    if (!token) {
      alert("Phiên đăng nhập hết hạn.");
      navigate('/login');
      return;
    }

    // Xác định thông tin giao hàng
    const finalShippingData = {
      name: isCustomShipping ? shippingForm.name : currentUser?.name,
      phone: isCustomShipping ? shippingForm.phone : currentUser?.phone,
      address: isCustomShipping ? shippingForm.address : currentUser?.address,
      email: currentUser?.email
    };

    if (!finalShippingData.name || !finalShippingData.phone || !finalShippingData.address) {
      alert("Vui lòng kiểm tra lại thông tin giao hàng!");
      return;
    }

    // Xác định nguồn gốc đơn hàng
    const isBuyNow = !location.state?.fromCart;

    // Payload chung
    const commonPayload = {
      access_token: token, // Gửi token trong body
      customer_info: finalShippingData,
      shipment: shippingMethod,
      payment_method: paymentMethod,
      total_amount: total
    };

    try {
      let data; // Biến lưu kết quả trả về

      if (isBuyNow) {
        // --- API MUA NGAY ---
        const payload = {
          ...commonPayload,
          item: {
            // Lấy phần tử đầu tiên vì mua ngay chỉ có 1 món
            productvariant_id: orderItems[0].variant_id || orderItems[0].productvariant_id,
            product_quantity: orderItems[0].product_quantity || orderItems[0].quantity
          }
        };
        // Gọi service
        data = await buyNow(payload);

      } else {
        // --- API THANH TOÁN GIỎ HÀNG ---
        const payload = {
          ...commonPayload,
          cart_items: orderItems.map(item => ({
            productvariant_id: item.variant_id || item.productvariant_id,
            product_quantity: item.product_quantity || item.quantity
          }))
        };
        // Gọi service
        data = await checkoutCart(payload);
      }

      alert(`Đặt hàng thành công! Mã đơn: #${data.order_id}`);

      navigate('/san-pham');

    } catch (error) {
      console.error("Lỗi đặt hàng:", error);
      // Hiển thị message lỗi chuẩn từ Backend
      alert(error.message || "Đặt hàng thất bại. Vui lòng thử lại.");
    }
  };

  if (orderItems.length === 0) return null;

  // Format tiền tệ
  // const formatCurrency = (amount) => new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(amount);
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

            {/* Thông tin giao hàng */}
            <div className="checkout-section">
              <h3>
                <FiMapPin style={{ marginRight: '8px', color: '#d49058' }} />
                Thông tin giao hàng
              </h3>

              {currentUser ? (
                <>
                  {/* Checkbox để chọn chế độ */}
                  <div style={{ marginBottom: '15px' }}>
                    <label style={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}>
                      <input
                        type="checkbox"
                        checked={isCustomShipping}
                        onChange={(e) => setIsCustomShipping(e.target.checked)}
                        style={{ marginRight: '8px', accentColor: '#d49058' }}
                      />
                      <strong>Giao hàng đến địa chỉ khác?</strong>
                    </label>
                  </div>

                  {/* LOGIC HIỂN THỊ: Nếu KHÔNG tích chọn -> Hiện thông tin mặc định */}
                  {!isCustomShipping ? (
                    <div className="default-address-card">
                      <p className="name"><strong>{currentUser.full_name}</strong></p>
                      <p className="phone">Số điện thoại: {currentUser.phone_number || "Chưa có SĐT"}</p>
                      <p className="address">Địa chỉ: {currentUser.address || "Chưa cập nhật địa chỉ"}</p>
                      <p className="email">Email: {currentUser.email}</p>

                      <Link to="/profile" style={{ fontSize: '0.9rem', color: '#d49058', marginTop: '0.5rem', display: 'inline-block' }}>
                        Thay đổi thông tin gốc
                      </Link>
                    </div>
                  ) : (
                    /* Nếu CÓ tích chọn -> Hiện Form nhập liệu */
                    <div className="custom-shipping-form" style={{ marginTop: '10px' }}>
                      <div style={{ marginBottom: '10px' }}>
                        <label>Tên người nhận:</label>
                        <input
                          type="text"
                          name="name"
                          value={shippingForm.name}
                          onChange={handleShippingChange}
                          placeholder="Nhập tên người nhận"
                          className="form-control"
                          style={{ width: '100%', padding: '8px', marginTop: '5px' }}
                        />
                      </div>

                      <div style={{ marginBottom: '10px' }}>
                        <label>Số điện thoại:</label>
                        <input
                          type="text"
                          name="phone"
                          value={shippingForm.phone}
                          onChange={handleShippingChange}
                          placeholder="Nhập số điện thoại"
                          className="form-control"
                          style={{ width: '100%', padding: '8px', marginTop: '5px' }}
                        />
                      </div>

                      <div style={{ marginBottom: '10px' }}>
                        <label>Địa chỉ nhận hàng:</label>
                        <textarea
                          name="address"
                          value={shippingForm.address}
                          onChange={handleShippingChange}
                          placeholder="Số nhà, tên đường, phường/xã..."
                          className="form-control"
                          rows="3"
                          style={{ width: '100%', padding: '8px', marginTop: '5px' }}
                        />
                      </div>
                    </div>
                  )}
                </>
              ) : (
                <p>Vui lòng đăng nhập để tải địa chỉ.</p>
              )}

            </div>

            {/* Phương thức vận chuyển */}
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

            {/* Phương thức thanh toán */}
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