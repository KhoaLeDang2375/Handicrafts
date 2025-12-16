import React, { useEffect, useState } from 'react';
import { getBlogs, createBlog, updateBlog, deleteBlog } from '../../services/blogApi';
import { FiEdit2, FiTrash2, FiPlus, FiSave, FiX } from 'react-icons/fi';
import './AdminBlogManager.scss';

const API_BASE = 'http://127.0.0.1:8000';

const AdminBlogManager = () => {
    // --- 1. KHAI BÁO STATE  ---
    const [blogs, setBlogs] = useState([]);
    const [title, setTitle] = useState('');
    const [content, setContent] = useState('');
    const [editingId, setEditingId] = useState(null);

    const [image, setImage] = useState(null); // State lưu file ảnh
    const [preview, setPreview] = useState(null); // Xem trước ảnh
    const [oldImage, setOldImage] = useState(null);

    const handleImageChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setImage(file);
            setPreview(URL.createObjectURL(file)); // Tạo link xem trước
        }
    };

    const token = localStorage.getItem('authToken');

    // Load dữ liệu khi vào trang
    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            const data = await getBlogs();
            console.log("Dữ liệu tải về từ server:", data);
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
                await updateBlog(editingId, title, content, image, token);
                alert("Cập nhật thành công!");
                setEditingId(null);
            } else {
                await createBlog(title, content, image, token);
                alert("Đăng bài thành công!");
            }

            // Reset form sau khi thành công
            setTitle('');
            setContent('');
            setImage(null);
            setPreview(null);
            window.location.reload();
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

        setOldImage(blog.image_url); // Lưu đường dẫn ảnh cũ
        console.log("Ảnh cũ",blog.image_url);
        setPreview(null); // Reset preview (vì chưa chọn ảnh mới)

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
        setOldImage(null); // Reset ảnh cũ
        setPreview(null);
        setImage(null);
    };

    return (
        <div className="admin-blog-container">
            <h2>Quản Lý Bài Viết Blog</h2>

            {/* --- FORM NHẬP LIỆU --- */}
            <div className="blog-form-card">
                <h3>{editingId ? 'Chỉnh sửa bài viết' : 'Tạo bài viết mới'}</h3>
                <form onSubmit={handleSubmit}>

                    {/* Input Ảnh */}
                    <div className="form-group">
                        <label>Hình ảnh minh họa:</label>
                        <input type="file" onChange={handleImageChange} accept="image/*" style={{ paddingLeft: '10px' }} />

                        <div style={{ marginTop: '10px' }}>
                            {preview ? (
                                // Trường hợp 1: vừa chọn file mới -> Hiện Preview
                                <div>
                                    <p style={{ fontSize: '1rem', color: '#666', marginBottom: '5px' }}>Ảnh mới</p>
                                    <img
                                        src={preview}
                                        alt="New Preview"
                                        style={{ width: '150px', height: 'auto', borderRadius: '4px', objectFit: 'cover' }}
                                    />
                                </div>
                            ) : (
                                // Trường hợp 2: Chưa chọn file mới -> Hiện ảnh cũ (nếu có)
                                oldImage && (
                                    <div>
                                        <p style={{ fontSize: '1rem', color: '#666', marginBottom: '5px' }}>Ảnh hiện tại:</p>
                                        <img
                                            src={`${API_BASE}${oldImage}`}
                                            alt="Current Blog"
                                            style={{ width: '150px', height: 'auto', borderRadius: '4px', objectFit: 'cover', border: '1px solid #ddd' }}

                                            // Xử lý trường hợp ảnh lỗi (ví dụ file bị xóa trên server)
                                            onError={(e) => {
                                                e.target.onerror = null;
                                                e.target.style.display = 'none'; 
                                            }}
                                        />
                                    </div>
                                )
                            )}
                        </div>
                    </div>

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