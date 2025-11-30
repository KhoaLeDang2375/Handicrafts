import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { FiPackage } from "react-icons/fi";
import { apiCall } from '../../services/api';
import './CartPage.scss';

import Logo from '../../assets/images/Aura.png';

const CartPage = () => {
    const [cartItems, setCartItems] = useState([]);
    // State lưu các ID của sản phẩm ĐƯỢC CHỌN (checkbox)
    const [selectedIds, setSelectedIds] = useState([]);
    const [loading, setLoading] = useState(true);

    // Hàm format tiền
    const formatCurrency = (amount) => new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(amount);

    // 1. Lấy dữ liệu từ Backend
    const fetchCart = async () => {
        try {
            const res = await apiCall('/my-cart/');
            const data = await res.json();
            if (data.items) setCartItems(data.items);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => { fetchCart(); }, []);

    // 2. Xử lý khi bấm Checkbox từng món
    const handleCheck = (id) => {
        if (selectedIds.includes(id)) {
            // Nếu đang chọn -> Bỏ chọn (Lọc bỏ ID ra khỏi mảng)
            setSelectedIds(selectedIds.filter(itemId => itemId !== id));
        } else {
            // Nếu chưa chọn -> Thêm vào mảng
            setSelectedIds([...selectedIds, id]);
        }
    };

    // 3. Xử lý Checkbox "Chọn tất cả"
    const handleUpdateQuantity = async (variantId, currentQty, change) => {
        const newQty = currentQty + change;
        if (newQty < 1) return; // Không cho giảm dưới 1

        // Tìm món hàng đang sửa để lấy thông tin tồn kho
        const currentItem = cartItems.find(item => item.productvariant_id === variantId);

        // KIỂM TRA TỒN KHO 
        if (change > 0 && currentItem && newQty > currentItem.stock_quantity) {
            alert(`Sản phẩm này chỉ còn ${currentItem.stock_quantity} món trong kho!`);
            return;
        }

        try {
            // Cập nhật giao diện ngay lập tức (Optimistic UI) cho mượt
            setCartItems(prev => prev.map(item =>
                item.productvariant_id === variantId
                    ? { ...item, product_quantity: newQty }
                    : item
            ));

            // Gọi API cập nhật ngầm
            await apiCall('/my-cart/update-item', {
                method: 'PUT',
                body: JSON.stringify({
                    productvariant_id: variantId,
                    product_quantity: newQty,
                    access_token: localStorage.getItem('authToken')
                })
            });
        } catch (error) {
            console.error("Lỗi cập nhật:", error);
            // Nếu lỗi thì load lại giỏ hàng cũ
            fetchCart();
        }
    };

    const handleRemoveItem = async (variantId) => {
        if (!window.confirm("Bạn có chắc muốn xóa sản phẩm này?")) return;

        try {
            // Xóa khỏi giao diện ngay
            setCartItems(prev => prev.filter(item => item.productvariant_id !== variantId));
            // Bỏ chọn nếu đang chọn
            setSelectedIds(prev => prev.filter(id => id !== variantId));

            // Gọi API xóa
            await apiCall(`/my-cart/remove-item/${variantId}`, {
                method: 'DELETE'
            });
        } catch (error) {
            console.error("Lỗi xóa:", error);
            fetchCart();
        }
    };

    // 4. Tính toán TỔNG TIỀN (Chỉ tính những món được chọn)
    const selectedItemsList = cartItems.filter(item => selectedIds.includes(item.productvariant_id));

    const subTotal = selectedItemsList.reduce((sum, item) => sum + (item.price * item.product_quantity), 0);
    const shippingFee = subTotal > 500000 ? 0 : 30000;
    // Logic: Nếu không có sản phẩm nào được chọn (length === 0) thì Tổng tiền = 0, Ngược lại thì cộng bình thường
    const finalTotal = selectedItemsList.length === 0 ? 0 : subTotal + shippingFee;
    return (
        <div className="cart-page">

            <div className="cart-container">
                <div className="cart-header">
                    <Link to="/san-pham" className="back-btn">
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="18"
                            height="18"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="2"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            style={{ marginRight: '8px' }} // Cách chữ ra một chút
                        >
                            <path d="M19 12H5"></path>
                            <path d="M12 19l-7-7 7-7"></path>
                        </svg>
                        Quay lại</Link>
                    <h1>Giỏ hàng của bạn</h1>
                </div>

                {cartItems.length === 0 ? (
                    <div className="empty-cart" style={{ textAlign: 'center', padding: '3rem' }}>
                        <p style={{ margin: '50px' }}>Giỏ hàng của bạn đang trống.</p>
                        <Link to="/san-pham" className="btn btn--primary">Mua sắm ngay</Link>
                    </div>
                ) : (

                    <div className="cart-layout">
                        {/* --- CỘT TRÁI: DANH SÁCH --- */}
                        <div className="cart-list">
                            {cartItems.map((item) => (
                                <div key={item.productvariant_id} className="cart-item">
                                    {/* CHECKBOX */}
                                    <div className="item-checkbox">
                                        <input
                                            type="checkbox"
                                            checked={selectedIds.includes(item.productvariant_id)}
                                            onChange={() => handleCheck(item.productvariant_id)}
                                        />
                                    </div>

                                    {/* <img src={item.image || {"https://via.placeholder.com/100"}} alt={item.product_name} */}

                                    <img src={Logo} alt={item.product_name} className="item-img" />

                                    <div className="item-info">
                                        <h3>{item.product_name}</h3>
                                        <div className="item-price">
                                            <span className="current">{formatCurrency(item.price)}</span>
                                            <span className="original">{formatCurrency(item.price * 1.2)}</span>
                                        </div>

                                        {/* Bộ điều khiển số lượng */}
                                        <div className="quantity-control-small">
                                            {/* Nút GIẢM: Truyền tham số -1 */}
                                            <button
                                                onClick={() => handleUpdateQuantity(item.productvariant_id, item.product_quantity, -1)}
                                                disabled={item.product_quantity <= 1} // Mờ nút nếu số lượng là 1
                                            >
                                                -
                                            </button>

                                            <span>{item.product_quantity}</span>

                                            {/* Nút TĂNG: Truyền tham số +1 */}
                                            <button
                                                onClick={() => handleUpdateQuantity(item.productvariant_id, item.product_quantity, 1)}
                                                disabled={item.product_quantity >= item.stock_quantity}
                                                style={{ opacity: item.product_quantity >= item.stock_quantity ? 0.5 : 1 }}
                                            >
                                                +
                                            </button>
                                        </div>
                                    </div>

                                    <div className="item-total-price">
                                        {formatCurrency(item.price * item.product_quantity)}
                                    </div>

                                    <button className="delete-btn" onClick={() => handleRemoveItem(item.productvariant_id)}>
                                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M3 6h18"></path><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
                                    </button>
                                </div>
                            ))}
                        </div>

                        {/* --- CỘT PHẢI: TỔNG KẾT --- */}
                        <div className="cart-summary">
                            <h3><FiPackage color="#DB9F6C" size="24px" /> Tổng đơn hàng</h3>

                            <div className="summary-row">
                                <span>Tạm tính ({selectedIds.length} sản phẩm)</span>
                                <span>{formatCurrency(subTotal)}</span>
                            </div>

                            <div className="summary-row">
                                <span>Phí vận chuyển</span>
                                <span>{formatCurrency(shippingFee)}</span>
                            </div>

                            <div className="summary-divider"></div>

                            <div className="summary-total">
                                <span>Tổng cộng</span>
                                <span className="total-price">{formatCurrency(finalTotal)}</span>
                            </div>

                            <button className="btn-checkout">Thanh toán</button>
                            <Link to="/san-pham" className="btn-continue">
                                Tiếp tục mua sắm
                            </Link>

                            <div className="cart-benefits">
                                <p>Thanh toán an toàn</p>
                                <p>Miễn phí đổi trả</p>
                                <p>Giao hàng nhanh</p>
                            </div>

                            <div className="promo-box">
                                <span className="promo-text">
                                    Miễn phí vận chuyển cho đơn hàng từ 500.000đ
                                </span>
                            </div>
                        </div>
                    </div>
                )}
            </div>

        </div>
    );
};

export default CartPage;