import { apiCall } from './api';

export const getAllProducts = async () => {
  // Gọi API lấy danh sách sản phẩm
  // apiCall đã tự xử lý check lỗi và parse JSON
  return await apiCall('/products', { method: 'GET' });
};

export const getProductById = async (id) => {
  return await apiCall(`/products/${id}`, { method: 'GET' });
};