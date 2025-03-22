# find-movies

Ứng dụng Python cho phép tìm kiếm thông tin phim, bao gồm tiêu đề, đạo diễn, diễn viên, đánh giá, và video YouTube, với đầu ra bằng tiếng Việt.

## Tính năng

- Tìm kiếm phim theo tên
- Hiển thị thông tin chi tiết về phim:
  - Tên phim
  - Đạo diễn
  - Diễn viên chính
  - Ngày phát hành
  - Xưởng phim/Hãng sản xuất
  - Thể loại
  - Đánh giá chi tiết từ nhiều nguồn (TMDB, IMDb, Rotten Tomatoes, Metacritic)
  - Đánh giá từ người xem (có dịch sang tiếng Việt)
  - Tóm tắt nội dung phim
  - Tóm tắt nội dung video YouTube đầu tiên (tự động)
  - Top 10 video YouTube liên quan
  - Link poster
  - Link IMDb

## Cấu trúc dự án

Dự án được tổ chức thành các module để dễ bảo trì và mở rộng:

```
mvp/
├── .env             # Chứa API keys thực tế (không được đưa lên GitHub)
├── .env.example     # Ví dụ mẫu về file .env (không chứa keys thật)
└── scripts/
    ├── api/               # Chứa các module API 
    │   ├── __init__.py
    │   ├── tmdb.py        # Xử lý API của The Movie Database
    │   ├── omdb.py        # Xử lý API của Open Movie Database
    │   └── youtube.py     # Xử lý API của YouTube và lấy phụ đề
    ├── utils/             # Chứa các module tiện ích
    │   ├── __init__.py
    │   ├── translator.py  # Hàm dịch thuật
    │   └── formatter.py   # Hàm định dạng và xử lý văn bản
    ├── config.py          # Cấu hình (API keys, URLs, hằng số)
    ├── main.py            # Điểm vào chương trình
    └── requirements.txt   # Thư viện cần thiết
```

## Yêu cầu

- Python 3.6 trở lên
- Các thư viện Python được liệt kê trong `requirements.txt`
- TMDB API key (đăng ký tại [themoviedb.org](https://www.themoviedb.org/settings/api))
- OMDb API key (đăng ký tại [omdbapi.com](https://www.omdbapi.com/apikey.aspx))
- YouTube API key (đăng ký tại [console.cloud.google.com](https://console.cloud.google.com/apis/library/youtube.googleapis.com))

## Cài đặt

1. Clone repository:
   ```bash
   git clone https://github.com/yourusername/find-movies.git
   cd find-movies
   ```

2. Cài đặt các thư viện cần thiết:
   ```bash
   pip install -r mvp/scripts/requirements.txt
   ```

3. Tạo file `.env` trong thư mục `mvp` dựa trên mẫu `.env.example`:
   ```bash
   cp mvp/.env.example mvp/.env
   ```

4. Thêm các API keys của bạn vào file `.env`:
   ```
   TMDB_API_KEY=your_tmdb_api_key_here
   OMDB_API_KEY=your_omdb_api_key_here
   YOUTUBE_API_KEY=your_youtube_api_key_here
   ```

## Cách sử dụng

1. Chạy script từ thư mục gốc của dự án:
   ```bash
   python mvp/scripts/main.py
   ```

2. Nhập tên phim cần tìm kiếm khi được yêu cầu.

3. Chọn một phim từ danh sách kết quả để xem thông tin chi tiết.

4. Thông tin sẽ được hiển thị bằng tiếng Việt, bao gồm:
   - Thông tin chi tiết về phim
   - Tóm tắt nội dung phim
   - Tóm tắt nội dung video YouTube đầu tiên (tự động trích xuất phụ đề)
   - Danh sách top 10 video YouTube liên quan

## Mở rộng

Script được thiết kế theo kiến trúc module, dễ dàng mở rộng:

1. **Thêm API mới**: Tạo module mới trong thư mục `api/` và thêm các hàm gọi API cần thiết
2. **Thêm tiện ích mới**: Tạo hoặc mở rộng module trong thư mục `utils/`
3. **Thay đổi cấu hình**: Cập nhật file `config.py` để thêm hằng số hoặc tham số mới
4. **Thay đổi giao diện**: Điều chỉnh hàm `display_movie_info()` trong `main.py`

## Thông tin về API

### The Movie Database (TMDB)
- TMDB là nguồn dữ liệu chính của script này
- API key miễn phí có thể nhận được bằng cách đăng ký tài khoản
- Giới hạn: 1,000 yêu cầu mỗi ngày

### Open Movie Database (OMDb)
- OMDb được sử dụng để lấy thông tin đánh giá từ IMDb, Rotten Tomatoes và Metacritic
- Cung cấp API key miễn phí với giới hạn 1,000 yêu cầu mỗi ngày
- Có thể mua gói trả phí nếu cần nhiều yêu cầu hơn

### YouTube Data API
- Được sử dụng để tìm kiếm video liên quan đến phim trên YouTube
- Cần đăng ký một dự án trên Google Cloud Console
- API key miễn phí cung cấp 10,000 đơn vị mỗi ngày (khoảng 100-150 yêu cầu)

## Chú ý

- Script này sử dụng TMDB API để lấy thông tin phim, OMDb API để lấy thông tin đánh giá, YouTube API để tìm video liên quan, YouTube Transcript API để lấy phụ đề, và dịch vụ Google Translate để dịch sang tiếng Việt.
- Tốc độ và chất lượng dịch có thể phụ thuộc vào kết nối mạng và hạn chế của API.
- Không phải tất cả các video YouTube đều có phụ đề. Nếu video không có phụ đề, tính năng tóm tắt nội dung video sẽ không hiển thị.
- Nếu không có OMDb API key, script vẫn hoạt động nhưng sẽ không hiển thị đánh giá từ IMDb, Rotten Tomatoes và Metacritic.
- Nếu không có YouTube API key, script sẽ chỉ hiển thị link tìm kiếm YouTube thay vì các video cụ thể.
