import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { FiUser, FiMail, FiPhone, FiMapPin, FiPackage, FiEdit3, FiLogOut, FiCamera } from 'react-icons/fi';
import { apiCall } from '../../services/api';
import './ProfilePage.scss';

import Logo from '../../assets/images/Aura.png';

const ProfilePage = () => {
    const [profile, setProfile] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchProfile = async () => {
            try {
                // 1. Gọi apiCall
                const response = await apiCall('/my-profile/', { method: 'GET' });

                // 2. Xử lý kết quả từ 'fetch'
                if (!response.ok) {
                    throw new Error(`Lỗi tải dữ liệu: ${response.statusText}`);
                }

                // 3. Giải nén JSON
                const data = await response.json();

                setProfile(data);
                setLoading(false);

            } catch (err) {
                console.error("Lỗi tại ProfilePage:", err);
                // Lưu ý: Lỗi 401 đã được api.js bắt và chuyển trang, nên ở đây chỉ bắt các lỗi khác
                if (err.message !== 'Phiên đăng nhập hết hạn') {
                    setError("Không thể tải thông tin. Vui lòng thử lại sau.");
                }
                setLoading(false);
            }
        };

        fetchProfile();
    }, []);

    const formatCurrency = (amount) => {
        return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(amount);
    };

    const formatDate = (dateString) => {
        if (!dateString) return '';
        const date = new Date(dateString);
        return date.toLocaleDateString('vi-VN');
    };

    const getStatusColor = (status) => {
        const s = status ? status.toLowerCase() : '';
        if (s === 'completed' || s === 'success') return 'bg-orange-100';
        if (s === 'pending' || s === 'processing') return 'bg-green-100';
        if (s === 'cancelled') return 'bg-gray-100';
        return 'bg-gray-100';
    };

    if (loading) return <div className="profile-container" style={{ justifyContent: 'center' }}>Đang tải dữ liệu...</div>;
    if (error) return <div className="profile-container" style={{ color: 'red' }}>{error}</div>;
    if (!profile) return null;

    return (
        <div className="profile-container">
            
            <div className="profile-sidebar">
                <div className="avatar-card">
                    <div className="avatar-circle">
                        {/* {profile.avatar_url ? (
                            <img src={profile.avatar_url} alt="Avatar" style={{ width: '100%', height: '100%', borderRadius: '50%', objectFit: 'cover' }} />
                        ) : (
                            profile.full_name ? profile.full_name.charAt(0).toUpperCase() : 'U'
                        )} */}
                        <img src={Logo} alt="Avatar" style={{ width: '100%', height: '100%', borderRadius: '50%', objectFit: 'cover' }} />
                       
                        <button className="camera-btn"><FiCamera size={14} /></button>
                    </div>

                    <h3>{profile.full_name}</h3>
                    <p className="sub-text">{profile.email}</p>

                    {/* Nút đăng xuất */}
                    <div className="logout-section" onClick={() => {
                        localStorage.removeItem('authToken');
                        localStorage.removeItem('userRole');
                        navigate('/login');
                    }}>
                        <FiLogOut style={{ marginRight: '5px' }} /> Đăng xuất
                    </div>
                </div>
            </div>

            {/* Content */}
            <div className="profile-content">
                <div className="content-card">
                    <div className="card-header">
                        <h3>Thông tin cá nhân</h3>
                        <button className="edit-btn"><FiEdit3 /> Chỉnh sửa</button>
                    </div>
                    <div className="info-grid">
                        <div className="info-item">
                            <label>Họ và tên</label>
                            <div className="input-box"><FiUser /> {profile.full_name}</div>
                        </div>
                        <div className="info-item">
                            <label>Email</label>
                            <div className="input-box"><FiMail /> {profile.email}</div>
                        </div>
                        <div className="info-item">
                            <label>Số điện thoại</label>
                            <div className="input-box"><FiPhone /> {profile.phone_number || "Chưa cập nhật"}</div>
                        </div>
                        <div className="info-item full-width">
                            <label>Địa chỉ</label>
                            <div className="input-box"><FiMapPin /> {profile.address || "Chưa cập nhật"}</div>
                        </div>
                    </div>
                </div>

                <div className="content-card mt-4">
                    <div className="card-header">
                        <h3><FiPackage style={{ marginRight: '8px', color: '#d49058' }} /> Lịch sử đơn hàng</h3>
                    </div>

                    {profile.orders && profile.orders.length > 0 ? (
                        <div className="order-list">
                            {profile.orders.map((order) => (
                                <div key={order.order_id} className="order-item">
                                    <div className="order-left">
                                        <span className="order-id">#{order.order_id}</span>
                                        <span className={`status-badge ${getStatusColor(order.status)}`}>
                                            {order.status}
                                        </span>
                                        <div className="order-meta">
                                            {formatDate(order.date)} &bull; {order.total_products} sản phẩm
                                        </div>
                                    </div>
                                    <div className="order-right">
                                        <span className="order-price">
                                            {formatCurrency(order.total_amount)}
                                        </span>
                                        <button className="detail-link">Chi tiết</button>
                                    </div>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <p style={{ color: '#666', fontStyle: 'italic' }}>Bạn chưa có đơn hàng nào.</p>
                    )}
                </div>
            </div>
        </div>
    );
};

export default ProfilePage;