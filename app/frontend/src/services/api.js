const BASE_URL = 'http://127.0.0.1:8000'; 

export const apiCall = async (endpoint, options = {}) => {
  // 1. Lấy token từ LocalStorage
  const token = localStorage.getItem('authToken');
  
  // 2. Chuẩn bị Header
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  const fullURL = `${BASE_URL}${endpoint}`;

  console.log(`%c Đang gọi API: ${fullURL}`, 'color: blue; font-weight: bold;');
  console.log("Dữ liệu gửi đi (Body):", options.body);

  try {
    const response = await fetch(fullURL, {
      ...options,
      headers,
    });

    console.log(`%c Kết quả từ Server: ${response.status}`, 'color: green; font-weight: bold;');

    // 3. Xử lý Token hết hạn (Lỗi 401)
    if (response.status === 401) {
      console.warn("Token hết hạn! Đang đăng xuất...");
      
      // Xóa SẠCH toàn bộ thông tin user
      localStorage.removeItem('authToken');
      localStorage.removeItem('userRole');
      localStorage.removeItem('currentUser'); 
      
      window.location.href = '/login';
      
      // Ném lỗi để dừng luồng xử lý hiện tại
      throw new Error('Phiên đăng nhập hết hạn. Vui lòng đăng nhập lại.');
    }

    // 4. Tự động đọc dữ liệu JSON
    const data = await response.json().catch(() => ({}));

    // 5. Xử lý các lỗi khác (400, 403, 404, 500...)
    if (!response.ok) {

      const errorMessage = data.detail || data.message || `Lỗi ${response.status}: ${response.statusText}`;

      // --- BẮT LỖI TOKEN HẾT HẠN KHI SERVER TRẢ VỀ 500 ---
      if (errorMessage.includes("Signature has expired")) {
          console.warn("Phát hiện Token hết hạn (qua thông báo lỗi). Đang đăng xuất...");
          localStorage.removeItem('authToken');
          localStorage.removeItem('userRole');
          localStorage.removeItem('currentUser');
          window.location.href = '/login';
          throw new Error('Phiên đăng nhập hết hạn.');
      }
      throw new Error(errorMessage);
    }

    // 6. Trả về DỮ LIỆU 
    return data;

  } catch (error) {

    console.error(`%c Lỗi API:`, 'color: red; font-weight: bold;', error.message);
    throw error;
  }
};