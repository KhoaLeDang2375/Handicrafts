import { apiCall } from './api';

export const getUserProfile = async () => {
    // Gọi API lấy thông tin cá nhân
    return await apiCall('/my-profile/', { method: 'GET' });
};