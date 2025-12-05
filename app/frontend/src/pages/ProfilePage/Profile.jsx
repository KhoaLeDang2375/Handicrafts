import React, { useState, useEffect } from 'react';
import { FiUser, FiMail, FiPhone, FiMapPin, FiPackage, FiEdit3 } from 'react-icons/fi';
import './ProfilePage.css'; // File CSS ở bước sau

const ProfilePage = () => {
  const [profile, setProfile] = useState(null);

  // Giả lập dữ liệu nhận từ API (Bạn sẽ thay bằng axios.get)
  useEffect(() => {
    // Mock data giống cấu trúc Backend trả về
    const mockData = {
      user_info: {
        name: "UserName",
        email: "Dan@gmail.com",
        phone: "0912 345 678",
        address: "123 Phố Cổ, Hoàn Kiếm, Hà Nội",
        join_date: "01/10/2024"
      },
      orders: [
        { id: "DH001", status: "Hoàn thành", date: "15/11/2024", total_products: 3, amount: 2150000 },
        { id: "DH002", status: "Đang xử lý", date: "20/11/2024", total_products: 1, amount: 850000 },
        { id: "DH003", status: "Hoàn thành", date: "25/11/2024", total_products: 2, amount: 1270000 },
      ]
    };
    setProfile(mockData);
  }, []);

  if (!profile) return <div>Loading...</div>;

  // Helper function để tô màu trạng thái
  const getStatusColor = (status) => {
    if (status === 'Hoàn thành') return 'bg-green-100 text-green-700';
    if (status === 'Đang xử lý') return 'bg-orange-100 text-orange-700';
    return 'bg-gray-100 text-gray-700';
  };

  return (
    <div className="profile-container">
      {/* Cột Trái: Avatar Card */}
      <div className="profile-sidebar">
        <div className="avatar-card">
            <div className="avatar-circle">
                {profile.user_info.name.charAt(0)}
                <button className="camera-btn">📷</button>
            </div>
            <h3>{profile.user_info.name}</h3>
            <p className="sub-text">{profile.user_info.email}</p>
            <p className="sub-text">📅 Tham gia: {profile.user_info.join_date}</p>
        </div>
      </div>

      {/* Cột Phải: Thông tin & Đơn hàng */}
      <div className="profile-content">
        
        {/* Card 1: Thông tin cá nhân */}
        <div className="content-card">
            <div className="card-header">
                <h3>Thông tin cá nhân</h3>
                <button className="edit-btn"><FiEdit3 /> Chỉnh sửa</button>
            </div>
            <div className="info-grid">
                <div className="info-item">
                    <label>Họ và tên</label>
                    <div className="input-box"><FiUser /> {profile.user_info.name}</div>
                </div>
                <div className="info-item">
                    <label>Email</label>
                    <div className="input-box"><FiMail /> {profile.user_info.email}</div>
                </div>
                <div className="info-item">
                    <label>Số điện thoại</label>
                    <div className="input-box"><FiPhone /> {profile.user_info.phone}</div>
                </div>
                <div className="info-item full-width">
                    <label>Địa chỉ</label>
                    <div className="input-box"><FiMapPin /> {profile.user_info.address}</div>
                </div>
            </div>
        </div>

        {/* Card 2: Lịch sử đơn hàng */}
        <div className="content-card mt-4">
            <div className="card-header">
                <h3><FiPackage style={{marginRight: '8px', color:'#d49058'}}/> Lịch sử đơn hàng</h3>
            </div>
            
            <div className="order-list">
                {profile.orders.map((order, index) => (
                    <div key={index} className="order-item">
                        <div className="order-left">
                            <span className="order-id">#{order.id}</span>
                            <span className={`status-badge ${getStatusColor(order.status)}`}>
                                {order.status}
                            </span>
                            <div className="order-meta">
                                📅 {order.date} &bull; {order.total_products} sản phẩm
                            </div>
                        </div>
                        <div className="order-right">
                            <span className="order-price">
                                {order.amount.toLocaleString('vi-VN')}đ
                            </span>
                            <button className="detail-link">Chi tiết</button>
                        </div>
                    </div>
                ))}
            </div>
        </div>

      </div>
    </div>
  );
};

export default ProfilePage;