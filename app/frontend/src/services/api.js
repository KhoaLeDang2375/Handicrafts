
const BASE_URL = 'http://127.0.0.1:8000'; 

export const apiCall = async (endpoint, options = {}) => {
  const token = localStorage.getItem('authToken');
  
  // 1. Sao chép options.headers (nếu có)
  const headers = { ...options.headers };

  // 2. LOGIC xử lý Content-Type
  // Nếu body là FormData -> không set Content-Type (để trình duyệt tự set)
  // Nếu body không phải FormData -> Set là application/json
  if (!(options.body instanceof FormData)) {
    headers['Content-Type'] = 'application/json';
  }

  // Thêm Token
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const fullURL = `${BASE_URL}${endpoint}`;

  console.log(`%c Gọi API: ${fullURL}`, 'color: blue');

  try {
    const response = await fetch(fullURL, {
      ...options,
      headers, // Header đã được xử lý chuẩn
    });

    // Xử lý 401 (Hết hạn token)
    if (response.status === 401) {
      console.warn("Token 401. Đăng xuất...");
      localStorage.clear(); 
      window.location.href = '/login';
      throw new Error('Phiên đăng nhập hết hạn.');
    }

    // Parse JSON
    const data = await response.json().catch(() => ({}));

    // Xử lý lỗi 
    if (!response.ok) {
      let errorMessage = `Lỗi ${response.status}: ${response.statusText}`;

      // Xử lý chi tiết lỗi từ FastAPI (tránh bị [object Object])
      if (data.detail) {
        if (typeof data.detail === 'string') {
          // Trường hợp lỗi đơn giản: "Token expired"
          errorMessage = data.detail;
        } else if (Array.isArray(data.detail)) {
          // Trường hợp lỗi Validation (422): data.detail là mảng
          // Ví dụ: "title: field required"
          errorMessage = data.detail
            .map(err => `${err.loc[1]}: ${err.msg}`)
            .join(', ');
        }
      }

      // Check lỗi chữ ký hết hạn (trường hợp server trả về 500)
      if (errorMessage.includes("Signature has expired")) {
        localStorage.clear();
        window.location.href = '/login';
        throw new Error('Phiên đăng nhập hết hạn.');
      }

      throw new Error(errorMessage);
    }

    return data;

  } catch (error) {
    console.error(`%c Lỗi API:`, 'color: red', error.message);
    throw error;
  }
};