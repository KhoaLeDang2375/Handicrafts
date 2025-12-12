import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getBlogById } from '../../services/blogApi';
import { FiUser, FiCalendar, FiClock } from 'react-icons/fi';
import './BlogDetailPage.scss';

const API_BASE = 'http://127.0.0.1:8000';

const BlogDetail = () => {
    const { id } = useParams();
    const [blog, setBlog] = useState(null);
    const [loading, setLoading] = useState(true);

    // --- State cho Comment Demo ---
    const [comments, setComments] = useState([
        { user: "Minh Anh", text: "Bài viết rất hữu ích!", time: "2 giờ trước" },
        { user: "Hoàng Nam", text: "Cảm ơn bạn đã chia sẻ.", time: "5 giờ trước" },
        { user: "Thu Hà", text: "Mình đã áp dụng và thấy rất hiệu quả!", time: "10 phút trước" },
        { user: "Quốc Bảo", text: "Thông tin quá chi tiết luôn.", time: "30 phút trước" },
        { user: "Lan Hương", text: "Bài viết chất lượng thật sự.", time: "1 giờ trước" },
        { user: "Hữu Đạt", text: "Cảm ơn tác giả nhiều nhé!", time: "3 giờ trước" },
        { user: "Phương Vy", text: "Mình đã lưu lại để xem tiếp.", time: "7 giờ trước" },
        { user: "Kim Yến", text: "Bài viết chi tiết quá trời.", time: "5 ngày trước" }
    ]);
    const [newComment, setNewComment] = useState("");

    useEffect(() => {
        const fetchDetail = async () => {
            try {
                const data = await getBlogById(id);
                setBlog(data);
            } catch (error) {
                console.error("Lỗi:", error);
            } finally {
                setLoading(false);
            }
        };
        fetchDetail();
    }, [id]);

    const handlePostComment = (e) => {
        e.preventDefault();
        if (!newComment.trim()) return;
        setComments([...comments, {
            user: "Bạn (Khách)",
            text: newComment,
            time: "Vừa xong"
        }]);
        setNewComment("");
    };

    if (loading) return <div className="detail-container">Đang tải...</div>;
    if (!blog) return <div className="detail-container">Không tìm thấy bài viết.</div>;

    return (
        <div className="detail-container">

            <div className="blog-layout">

                {/* CỘT TRÁI: Nội dung bài viết */}
                <div className="left-column">
                    <article className="blog-article">
                        <h1 className="article-title">{blog.title}</h1>

                        <div className="article-meta">
                            <span><FiUser /> {blog.author_name || "Admin"}</span>
                            <span><FiCalendar /> {blog.create_time ? new Date(blog.create_time).toLocaleDateString('vi-VN') : ''}</span>
                        </div>

                        {blog.image_url && (
                            <div className="article-image">
                                <img
                                    src={`${API_BASE}${blog.image_url}`}
                                    alt={blog.title}
                                    onError={(e) => { e.target.style.display = 'none' }}
                                />
                            </div>
                        )}

                        <div className="article-content">
                            {blog.content.split('\n').map((line, idx) => (
                                <p key={idx}>{line}</p>
                            ))}
                        </div>
                    </article>
                </div>

                {/* CỘT PHẢI: Bình luận*/}
                <div className="right-column">
                    <div className="comment-box">
                        <h3>Bình luận ({comments.length})</h3>

                        <form className="comment-form" onSubmit={handlePostComment}>
                            <textarea
                                placeholder="Chia sẻ ý kiến của bạn..."
                                value={newComment}
                                onChange={(e) => setNewComment(e.target.value)}
                            ></textarea>
                            <button type="submit">Gửi</button>
                        </form>

                        <div className="comment-list">
                            {comments.map((cmt, index) => (
                                <div key={index} className="comment-item">
                                    <div className="cmt-avatar">{cmt.user.charAt(0)}</div>
                                    <div className="cmt-body">
                                        <div className="cmt-header">
                                            <strong>{cmt.user}</strong>
                                            <small>{cmt.time}</small>
                                        </div>
                                        <p>{cmt.text}</p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

            </div>

        </div>
    );
};

export default BlogDetail;