import { apiCall } from './api';

// 1. Hàm thanh toán cho giỏ hàng
export const checkoutCart = async (payload) => {
  return await apiCall('/orders/checkout', {
    method: 'POST',
    body: JSON.stringify(payload)
  });
};

// 2. hàm mua ngay (1 món)
export const buyNow = async (payload) => {
  return await apiCall('/orders/buy-now', {
    method: 'POST',
    body: JSON.stringify(payload)
  });
};