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
  - Tóm tắt nội dung phim
  - Tóm tắt nội dung video YouTube đầu tiên (tự động)
  - Top 10 video YouTube liên quan
  - Link poster
  - Link IMDb

## Yêu cầu

- Python 3.6 trở lên
- Các thư viện Python được liệt kê trong `requirements.txt`
- TMDB API key (đăng ký tại [themoviedb.org](https://www.themoviedb.org/settings/api))
- OMDb API key (đăng ký tại [omdbapi.com](https://www.omdbapi.com/apikey.aspx)) - *Tùy chọn nhưng khuyến khích*
- YouTube API key (đăng ký tại [console.cloud.google.com](https://console.cloud.google.com/apis/library/youtube.googleapis.com)) - *Tùy chọn nhưng khuyến khích*

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

4. Thông tin sẽ được hiển thị bằng tiếng Việt, bao gồm:
   - Thông tin chi tiết về phim
   - Tóm tắt nội dung phim
   - Tóm tắt nội dung video YouTube đầu tiên (tự động trích xuất phụ đề)
   - Danh sách top 10 video YouTube liên quan

## Thứ tự hiển thị thông tin

Script hiển thị thông tin theo thứ tự sau:
1. Thông tin cơ bản (tên, ngày phát hành, thể loại, đạo diễn, diễn viên)
2. Đánh giá từ các nguồn (TMDB, IMDb, Rotten Tomatoes, Metacritic)
3. Đánh giá từ người xem
4. Tóm tắt nội dung phim
5. Tóm tắt nội dung video YouTube đầu tiên (nếu có)
6. Danh sách các video YouTube liên quan
7. Link poster

## Tìm kiếm YouTube

Script tự động tìm kiếm video liên quan trên YouTube bằng từ khóa mặc định: "[tên phim] review đánh giá phim"

Mỗi kết quả đều hiển thị:
- Tiêu đề video
- Tên kênh
- Ngày đăng
- Link trực tiếp đến video

## Tính năng phụ đề YouTube

Script tự động trích xuất phụ đề từ video YouTube đầu tiên trong kết quả tìm kiếm:

1. **Trích xuất tự động**: Lấy phụ đề video đầu tiên (nếu có) và hiển thị tóm tắt
2. **Ưu tiên phụ đề tiếng Việt**: Nếu video có phụ đề tiếng Việt, sẽ sử dụng phụ đề đó
3. **Tự động dịch**: Nếu chỉ có phụ đề tiếng Anh, sẽ tự động dịch sang tiếng Việt
4. **Tóm tắt thông minh**: Hiển thị 3 câu đầu tiên của phụ đề để nắm được nội dung chính

Tính năng này giúp hiểu nhanh nội dung video mà không cần phải xem.

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

- Script này sử dụng TMDB API để lấy thông tin phim, OMDb API để lấy thông tin đánh giá, YouTube API để tìm video liên quan, YouTube Transcript API để lấy phụ đề, và dịch vụ Google Translate để dịch sang tiếng Việt.
- Tốc độ và chất lượng dịch có thể phụ thuộc vào kết nối mạng và hạn chế của API.
- Không phải tất cả các video YouTube đều có phụ đề. Nếu video không có phụ đề, tính năng tóm tắt nội dung video sẽ không hiển thị.
- Nếu không có OMDb API key, script vẫn hoạt động nhưng sẽ không hiển thị đánh giá từ IMDb, Rotten Tomatoes và Metacritic.
- Nếu không có YouTube API key, script sẽ chỉ hiển thị link tìm kiếm YouTube thay vì các video cụ thể. 