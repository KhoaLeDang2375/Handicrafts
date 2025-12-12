import { apiCall } from './api';

// Lấy danh sách blog
export const getBlogs = async () => {
  return await apiCall('/blogs/?skip=0&limit=100');
};

// Tạo blog (Backend yêu cầu token trên URL)
export const createBlog = async (title, content, token) => {
  return await apiCall(`/blogs/?access_token=${token}`, {
    method: 'POST',
    body: JSON.stringify({ title, content })
  });
};

// Sửa blog
export const updateBlog = async (id, title, content, token) => {
  return await apiCall(`/blogs/${id}?access_token=${token}`, {
    method: 'PUT',
    body: JSON.stringify({ title, content })
  });
};

// Xóa blog
export const deleteBlog = async (id, token) => {
  return await apiCall(`/blogs/${id}?access_token=${token}`, {
    method: 'DELETE',
  });
};