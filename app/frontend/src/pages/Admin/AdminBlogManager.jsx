import React, { useEffect, useState } from 'react';
import { getBlogs, createBlog, updateBlog, deleteBlog } from '../../services/blogApi';
import { FiEdit2, FiTrash2, FiPlus, FiSave, FiX } from 'react-icons/fi';
import './AdminBlogManager.scss';

const AdminBlogManager = () => {
    // --- 1. KHAI BÁO STATE (Phải nằm đầu tiên) ---
    const [blogs, setBlogs] = useState([]);
    const [title, setTitle] = useState('');
    const [content, setContent] = useState('');
    const [editingId, setEditingId] = useState(null);

    const token = localStorage.getItem('authToken');

    // Load dữ liệu khi vào trang
    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            const data = await getBlogs();
            setBlogs(data);
        } catch (error) {
            console.error(error);
        }
    };

    // --- 2. HÀM XỬ LÝ SUBMIT ---
    const handleSubmit = async (e) => {
        e.preventDefault();

        // Kiểm tra biến title và content có tồn tại không trước khi dùng .trim()
        if (!title || !title.trim()) return alert("Vui lòng nhập tiêu đề");
        if (!content || !content.trim()) return alert("Vui lòng nhập nội dung");

        try {
            if (editingId) {
                // Cập nhật bài viết (Gửi cả ID, Title, Content, Token)
                await updateBlog(editingId, title, content, token);
                alert("Cập nhật thành công!");
                setEditingId(null);
            } else {
                // Tạo bài viết mới (Gửi Title, Content, Token)
                await createBlog(title, content, token);
                alert("Đăng bài thành công!");
            }

            // Reset form sau khi thành công
            setTitle('');
            setContent('');
            fetchData(); // Load lại danh sách
        } catch (error) {
            // In lỗi ra console để debug nếu có
            console.error("Submit Error:", error);
            alert("Lỗi: " + (error.message || "Có lỗi xảy ra"));
        }
    };

    // --- 3. HÀM XỬ LÝ CLICK SỬA ---
    const handleEditClick = (blog) => {
        setEditingId(blog.id);
        setTitle(blog.title || ''); // Đổ dữ liệu cũ vào ô input
        setContent(blog.content || '');
        // Cuộn lên đầu trang
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    const handleDeleteClick = async (id) => {
        if (window.confirm("Bạn có chắc muốn xóa bài viết này?")) {
            try {
                await deleteBlog(id, token);
                fetchData();
            } catch (error) {
                alert("Xóa thất bại: " + error.message);
            }
        }
    };

    const cancelEdit = () => {
        setEditingId(null);
        setTitle('');
        setContent('');
    };

    return (
        <div className="admin-blog-container">
            <h2>Quản Lý Bài Viết Blog</h2>

            {/* --- FORM NHẬP LIỆU --- */}
            <div className="blog-form-card">
                <h3>{editingId ? 'Chỉnh sửa bài viết' : 'Tạo bài viết mới'}</h3>
                <form onSubmit={handleSubmit}>

                    <div className="form-group">
                        <label>Tiêu đề:</label>
                        <input
                            type="text"
                            className="title-input"
                            placeholder="Nhập tiêu đề bài viết..."
                            value={title}
                            onChange={(e) => setTitle(e.target.value)}
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label>Nội dung:</label>
                        <textarea
                            rows="5"
                            placeholder="Nhập nội dung bài viết..."
                            value={content}
                            onChange={(e) => setContent(e.target.value)}
                            required
                        ></textarea>
                    </div>

                    <div className="form-actions">
                        <button type="submit" className={`btn-save ${editingId ? 'update' : 'create'}`}>
                            {editingId ? <><FiSave /> Lưu Cập Nhật</> : <><FiPlus /> Đăng Bài</>}
                        </button>

                        {editingId && (
                            <button type="button" onClick={cancelEdit} className="btn-cancel">
                                <FiX /> Hủy
                            </button>
                        )}
                    </div>
                </form>
            </div>

            {/* --- DANH SÁCH BÀI VIẾT --- */}
            <div className="blog-list-admin">
                <h3>Danh sách bài viết hiện có ({blogs.length})</h3>
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Tiêu đề</th>
                            <th>Nội dung (Tóm tắt)</th>
                            <th>Hành động</th>
                        </tr>
                    </thead>
                    <tbody>
                        {blogs.map(blog => (
                            <tr key={blog.id}>
                                <td>#{blog.id}</td>
                                <td style={{ fontWeight: 'bold', color: '#d4a768' }}>
                                    {blog.title || "(Không có tiêu đề)"}
                                </td>
                                <td className="content-cell">
                                    {blog.content.length > 50 ? blog.content.substring(0, 50) + '...' : blog.content}
                                </td>
                                <td className="action-cell">
                                    <button className="btn-icon edit" onClick={() => handleEditClick(blog)}>
                                        <FiEdit2 />
                                    </button>
                                    <button className="btn-icon delete" onClick={() => handleDeleteClick(blog.id)}>
                                        <FiTrash2 />
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default AdminBlogManager;