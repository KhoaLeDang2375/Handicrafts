# Handicraft E-commerce Website

## Mô tả dự án

Đây là một website kinh doanh sản phẩm thủ công mỹ nghệ được xây dựng với kiến trúc full-stack. Dự án bao gồm backend API được phát triển bằng FastAPI (Python) và frontend giao diện người dùng được xây dựng bằng React với Vite. Hệ thống sử dụng MySQL làm cơ sở dữ liệu để lưu trữ thông tin sản phẩm, người dùng, đơn hàng và các dữ liệu liên quan.

## Tính năng chính

- **Quản lý sản phẩm**: Hiển thị, tìm kiếm và chi tiết sản phẩm thủ công mỹ nghệ
- **Hệ thống người dùng**: Đăng ký, đăng nhập, quản lý hồ sơ cá nhân
- **Giỏ hàng và thanh toán**: Thêm sản phẩm vào giỏ, đặt hàng và thanh toán
- **Quản lý đơn hàng**: Theo dõi trạng thái đơn hàng, lịch sử mua hàng
- **Blog và đánh giá**: Chia sẻ bài viết về thủ công mỹ nghệ và đánh giá sản phẩm
- **Liên hệ**: Form liên hệ cho khách hàng
- **Admin panel**: Quản lý sản phẩm, đơn hàng, blog từ phía admin

## Công nghệ sử dụng

### Backend
- **Python 3.x**
- **FastAPI**: Framework API nhanh và hiện đại
- **MySQL**: Cơ sở dữ liệu quan hệ
- **PyMySQL**: Driver kết nối MySQL
- **Pydantic**: Validation dữ liệu
- **Bcrypt/Passlib**: Mã hóa mật khẩu
- **Uvicorn**: ASGI server

### Frontend
- **React**: Library JavaScript cho giao diện người dùng
- **Vite**: Build tool và dev server nhanh
- **SCSS**: Preprocessor CSS
- **Axios**: HTTP client cho API calls

## Cài đặt và chạy dự án

### Yêu cầu hệ thống
- Python 3.8+
- Node.js 16+
- MySQL 8.0+
- Git

### 1. Clone repository
```bash
git clone <repository-url>
cd handicraft_project
```

### 2. Cài đặt và cấu hình cơ sở dữ liệu

#### Tạo database MySQL
```sql
CREATE DATABASE handicraft_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### Khôi phục dữ liệu từ file backup
Giả sử bạn có file `handicraft_backup.sql`:
```bash
mysql -u <username> -p handicraft_db < handicraft_backup.sql
```

### 3. Cấu hình backend

#### Tạo file môi trường
Tạo file `.env` trong thư mục gốc với nội dung:
```env
DB_HOST=localhost
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=handicraft_db
```

#### Cài đặt dependencies Python
```bash
pip install -r requirements.txt
```

#### Chạy backend server
```bash
python main.py
```
hoặc
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

API sẽ chạy tại: http://localhost:8000
API Documentation: http://localhost:8000/docs

### 4. Cấu hình frontend

#### Cài đặt dependencies Node.js
```bash
cd frontend
npm install
```

#### Chạy frontend development server
```bash
npm run dev
```

Frontend sẽ chạy tại: http://localhost:5173 (mặc định của Vite)

## Tài nguyên bổ sung

### File Backup Database
File backup MySQL của dự án có thể tải xuống từ Google Drive:
- [Download Backup Database](https://drive.google.com/file/d/15COTyryE-OCiXU-sGf2Q0FliHuVkWRJB/view?usp=sharing)

### Demo Chức năng
Video demo các chức năng của website:
- [Xem Demo Chức năng](https://drive.google.com/drive/folders/1lmdNO_9wccwiE81Ac3PMYMzXH0kQ1bkT?usp=drive_link)

## Cấu trúc dự án

```
handicraft_project/
├── main.py                 # Entry point của FastAPI app
├── config.py               # Cấu hình ứng dụng
├── requirements.txt        # Dependencies Python
├── gen_password_test.py    # Script test mật khẩu
├── app/
│   ├── __init__.py
│   ├── database.py         # Kết nối và thao tác database
│   ├── schemas.py          # Pydantic schemas
│   ├── security.py         # Xác thực và bảo mật
│   ├── models/             # SQLAlchemy models (nếu có)
│   ├── routes/             # API endpoints
│   ├── static/             # Static files (images, etc.)
│   └── templates/          # HTML templates (nếu có)
├── frontend/
│   ├── index.html
│   ├── vite.config.js
│   ├── package.json
│   ├── src/
│   │   ├── main.jsx
│   │   ├── App.jsx
│   │   ├── components/     # React components
│   │   ├── pages/          # Các trang của website
│   │   ├── services/       # API service functions
│   │   └── scss/           # Stylesheets
│   └── public/             # Static assets
├── search_service/         # Dịch vụ tìm kiếm
└── __pycache__/            # Python cache files
```

## API Endpoints

Dự án bao gồm các API endpoints chính:

- `/api/products` - Quản lý sản phẩm
- `/api/auth` - Xác thực người dùng (login/signup)
- `/api/cart` - Giỏ hàng
- `/api/orders` - Đơn hàng
- `/api/reviews` - Đánh giá sản phẩm
- `/api/blogs` - Bài viết blog
- `/api/contact` - Liên hệ

Chi tiết API documentation có thể xem tại `/docs` khi server đang chạy.

## Triển khai production

### Backend
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend
```bash
npm run build
npm run preview
```

## Đóng góp

1. Fork dự án
2. Tạo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## Tác giả

- **Lê Đăng Khoa** - *Backend Developer* - [GitHub Profile](https://github.com/KhoaLeDang2375)
- **Huỳnh Thanh Dân** - *Frontend Developer* - [GitHub Profile](https://github.com/HuynhThanhDan-23520220)


## Giấy phép

Dự án này được phân phối dưới giấy phép MIT. Xem file `LICENSE` để biết thêm chi tiết.

## Liên hệ

- Email: ledangkhoa11a1@gmail.com
- Project Link: [https://github.com/username/handicraft-project](https://github.com/username/handicraft-project)

---

*Được phát triển với ❤️ cho cộng đồng thủ công mỹ nghệ*</content>
<parameter name="filePath">/home/handicraft/handicraft_project/README.md