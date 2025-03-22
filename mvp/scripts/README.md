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
  - Đánh giá chi tiết từ nhiều nguồn (TMDB, IMDb, Rotten Tomatoes, Metacritic)
  - Đánh giá từ người xem (có dịch sang tiếng Việt)
  - Top 10 video YouTube liên quan (với từ khóa tùy chỉnh)
  - Tóm tắt nội dung
  - Link poster
  - Link IMDb

## Yêu cầu

- Python 3.6 trở lên
- Các thư viện Python được liệt kê trong `requirements.txt`
- TMDB API key (đăng ký tại [themoviedb.org](https://www.themoviedb.org/settings/api))
- OMDb API key (đăng ký tại [omdbapi.com](https://www.omdbapi.com/apikey.aspx)) - *Tùy chọn nhưng khuyến khích*
- YouTube Data API key (đăng ký tại [console.cloud.google.com](https://console.cloud.google.com/apis/library/youtube.googleapis.com)) - *Tùy chọn nhưng khuyến khích*

## Cài đặt

1. Cài đặt các thư viện cần thiết:

```bash
pip install -r requirements.txt
```

2. Mở file `movie_search.py` và thay đổi giá trị của các biến API key:

```python
TMDB_API_KEY = "your_tmdb_api_key_here"  # Thay thế bằng TMDB API key của bạn
OMDB_API_KEY = "your_omdb_api_key_here"  # Thay thế bằng OMDb API key của bạn
YOUTUBE_API_KEY = "your_youtube_api_key_here"  # Thay thế bằng YouTube API key của bạn
```

## Cách sử dụng

1. Chạy script:

```bash
python movie_search.py
```

2. Nhập tên phim cần tìm kiếm khi được yêu cầu.

3. Chọn một phim từ danh sách kết quả để xem thông tin chi tiết.

4. Khi được nhắc, bạn có thể nhập từ khóa tùy chỉnh để tìm kiếm video trên YouTube:
   - Để trống: dùng từ khóa mặc định "[tên phim] review đánh giá phim" 
   - Nhập từ khóa: tìm kiếm "[tên phim] [từ khóa của bạn]"

5. Thông tin sẽ được hiển thị bằng tiếng Việt, bao gồm top 10 video YouTube liên quan.

## Tìm kiếm YouTube

Script tìm kiếm và hiển thị top 10 video YouTube liên quan đến phim:

1. **Tự động với từ khóa mặc định**: Khi để trống cửa sổ nhập từ khóa, script sẽ tìm kiếm sử dụng "[tên phim] review đánh giá phim"

2. **Tùy chỉnh từ khóa**: Bạn có thể nhập từ khóa riêng, ví dụ:
   - "review" - tìm review đơn giản
   - "trailer" - tìm trailer phim
   - "phân tích" - tìm video phân tích phim
   - "cảnh hay" - tìm cảnh đáng nhớ
   - "hậu trường" - tìm video hậu trường
   - "phỏng vấn" - tìm phỏng vấn diễn viên, đạo diễn

Từ khóa của bạn sẽ được kết hợp với tên phim: "[tên phim] [từ khóa của bạn]"

Mỗi kết quả đều hiển thị:
- Tiêu đề video
- Tên kênh
- Ngày đăng
- Link trực tiếp đến video

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

## Lưu ý

- Script này sử dụng TMDB API để lấy thông tin phim, OMDb API để lấy thông tin đánh giá, YouTube API để tìm video liên quan, và dịch vụ Google Translate để dịch sang tiếng Việt.
- Tốc độ và chất lượng dịch có thể phụ thuộc vào kết nối mạng và hạn chế của API.
- Nếu không có OMDb API key, script vẫn hoạt động nhưng sẽ không hiển thị đánh giá từ IMDb, Rotten Tomatoes và Metacritic.
- Nếu không có YouTube API key, script sẽ chỉ hiển thị link tìm kiếm YouTube thay vì các video cụ thể. 