import { apiCall } from './api';

export const getCart = async () => {
  // apiCall tự động lấy token từ localStorage và gắn vào Header
  return await apiCall('/my-cart/', { method: 'GET' });
};

// 1. Thêm vào giỏ hàng
export const addToCart = async (variantId, quantity, token) => {
  return await apiCall('/my-cart/add-item', {
    method: 'POST',
    body: JSON.stringify({
      productvariant_id: variantId,
      product_quantity: quantity,
      access_token: token
    })
  });
};

// 2. Cập nhật số lượng (PUT)
export const updateCartItem = async (variantId, quantity) => {
  const token = localStorage.getItem('authToken');
  return await apiCall('/my-cart/update-item', {
    method: 'PUT',
    body: JSON.stringify({
      productvariant_id: variantId,
      product_quantity: quantity,
      access_token: token 
    })
  });
};

// 3. Xóa sản phẩm (DELETE)
export const removeCartItem = async (variantId) => {
  return await apiCall(`/my-cart/remove-item/${variantId}`, {
    method: 'DELETE'
  });
};