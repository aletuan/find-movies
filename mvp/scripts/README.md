# Movie Search Script

Đây là script Python cho phép tìm kiếm phim và hiển thị thông tin chi tiết về phim bằng tiếng Việt.

## Tính năng

- Tìm kiếm phim theo tên
- Hiển thị thông tin chi tiết về phim:
  - Tên phim
  - Đạo diễn
  - Diễn viên chính
  - Ngày phát hành
  - Xưởng phim/Hãng sản xuất
  - Thể loại
  - Đánh giá
  - Tóm tắt nội dung
  - Link poster

## Yêu cầu

- Python 3.6 trở lên
- Các thư viện Python được liệt kê trong `requirements.txt`
- TMDB API key (đăng ký tại [themoviedb.org](https://www.themoviedb.org/settings/api))

## Cài đặt

1. Cài đặt các thư viện cần thiết:

```bash
pip install -r requirements.txt
```

2. Mở file `movie_search.py` và thay đổi giá trị của biến `TMDB_API_KEY` với API key của bạn:

```python
TMDB_API_KEY = "y12d8852faa36602d14b98d24eecc10de"  # Thay thế bằng TMDB API key của bạn
```

## Cách sử dụng

1. Chạy script:

```bash
python movie_search.py
```

2. Nhập tên phim cần tìm kiếm khi được yêu cầu.

3. Chọn một phim từ danh sách kết quả để xem thông tin chi tiết.

4. Thông tin sẽ được hiển thị bằng tiếng Việt.

## Lưu ý

- Script này sử dụng TMDB API để lấy thông tin phim, và dịch vụ Google Translate để dịch sang tiếng Việt.
- Tốc độ và chất lượng dịch có thể phụ thuộc vào kết nối mạng và hạn chế của API. 