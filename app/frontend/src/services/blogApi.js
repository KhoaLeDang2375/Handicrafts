import { apiCall } from './api';

// Lấy danh sách blog
export const getBlogs = async () => {
  return await apiCall('/blogs/?skip=0&limit=100');
};


export const createBlog = async (title, content, imageFile, token) => {
  const formData = new FormData();
  formData.append('title', title);
  formData.append('content', content);

  // Chỉ append nếu có ảnh
  if (imageFile) {
    formData.append('image', imageFile);
  }

  // Gọi apiCall, truyền formData vào body
  // apiCall sẽ tự động phát hiện đây là FormData và KHÔNG chèn application/json
  return await apiCall(`/blogs/?access_token=${token}`, {
    method: 'POST',
    body: formData
  });
};

// Sửa blog
export const updateBlog = async (id, title, content, imageFile, token) => {
  const formData = new FormData();
  formData.append('title', title);
  formData.append('content', content);
  
  // Chỉ gửi ảnh nếu người dùng chọn ảnh mới
  if (imageFile) {
    formData.append('image', imageFile);
  }

  // Gửi FormData (apiCall sẽ tự động xử lý header)
  return await apiCall(`/blogs/${id}?access_token=${token}`, {
    method: 'PUT',
    body: formData 
  });
};

// Xóa blog
export const deleteBlog = async (id, token) => {
  return await apiCall(`/blogs/${id}?access_token=${token}`, {
    method: 'DELETE',
  });
};

export const getBlogById = async (id) => {
  // Gọi API: GET /blogs/{id}
  return await apiCall(`/blogs/${id}`, { 
    method: 'GET' 
  });
};