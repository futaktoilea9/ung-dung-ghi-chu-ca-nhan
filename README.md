# Ứng Dụng Ghi Chú Cá Nhân

Ứng dụng Flask + SQLite tạo, tìm kiếm, gắn thẻ và lưu trữ ghi chú cá nhân.

## Tính năng

- Tạo và lưu ghi chú cá nhân bằng SQLite
- Gắn thẻ, ghim, lưu trữ và tìm kiếm ghi chú
- REST API thống kê ghi chú theo trạng thái

## Công nghệ

- Python 3.11+
- Flask
- SQLite
- Pytest
- HTML/CSS dashboard

## Chạy dự án

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Mặc định ứng dụng chạy ở `http://localhost:5003`.

## API chính

- `GET /health` - kiểm tra trạng thái ứng dụng
- `GET /api/stats` - thống kê tổng quan
- `GET /api/items` - danh sách dữ liệu mới nhất

## Kiểm thử

```bash
python -m pytest -q
```

## Cấu trúc

```text
.
├── app.py
├── requirements.txt
├── templates/index.html
├── static/style.css
└── tests/test_app.py
```

Dự án này sử dụng SQLite nội bộ và tự tạo dữ liệu mẫu khi khởi động.
