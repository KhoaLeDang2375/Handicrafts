// src/services/api.js

const BASE_URL = 'http://127.0.0.1:8000'; 

export const apiCall = async (endpoint, options = {}) => {
  // 1. Lấy token
  const token = localStorage.getItem('authToken');
  
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const fullURL = `${BASE_URL}${endpoint}`;

  // --- DEBUG LOG (Xem tại Console trình duyệt F12) ---
  console.log(`%c Đang gọi API: ${fullURL}`, 'color: blue; font-weight: bold;');
  console.log("Dữ liệu gửi đi (Body):", options.body);
  console.log("Token đang dùng:", token);
  // --------------------------------------------------

  try {
    const response = await fetch(fullURL, {
      ...options,
      headers,
    });

    // --- DEBUG LOG ---
    console.log(`%c Kết quả từ Server: ${response.status}`, 'color: green; font-weight: bold;');
    // -----------------

    if (response.status === 401) {
      console.warn("Token hết hạn! Đang đăng xuất...");
      localStorage.removeItem('authToken');
      localStorage.removeItem('userRole');
      window.location.href = '/login';
      throw new Error('Phiên đăng nhập hết hạn');
    }

    return response;

  } catch (error) {
    // --- DEBUG LOG ---
    console.error(`%c Lỗi gọi API (Fetch Error):`, 'color: red; font-weight: bold;', error);
    // -----------------
    throw error;
  }
};