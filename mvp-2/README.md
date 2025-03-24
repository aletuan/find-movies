# Movie Search and Analysis

Ứng dụng tìm kiếm và phân tích phim sử dụng OMDb API cho dữ liệu phim và OpenAI API cho phân tích chuyên sâu.

## Tính năng

- Tìm kiếm thông tin phim:
  - Tìm kiếm bằng tên tiếng Việt hoặc tiếng Anh
  - Tự động dịch tên phim sang tiếng Anh nếu không tìm thấy kết quả
  - Kiểm tra và xác thực input người dùng
  - Hiển thị kết quả tìm kiếm dạng bảng với thông tin tổng quan

- Hiển thị thông tin chi tiết phim:
  - Thông tin cơ bản: tên, năm, thời lượng, thể loại, đạo diễn, diễn viên
  - Đánh giá từ nhiều nguồn: IMDb, Rotten Tomatoes, Metacritic
  - Phân tích giải thưởng chi tiết:
    - Phân loại theo Oscar, Quả Cầu Vàng, BAFTA và các giải khác
    - Hiển thị chi tiết hạng mục và kết quả
    - Tóm tắt thành tựu nổi bật
    - Thống kê tổng số giải thắng và đề cử
  - Phân tích chuyên sâu bằng AI:
    - Bối cảnh và vị trí của phim trong thể loại
    - Phân tích kịch bản và phát triển nhân vật
    - Đánh giá về diễn xuất và đạo diễn
    - Nhận xét về giá trị nghệ thuật và đối tượng phù hợp
  - Link poster phim

- Giao diện:
  - Sử dụng Rich để tạo giao diện console đẹp mắt
  - Màu sắc và biểu tượng trực quan
  - Định dạng bảng và panel cho thông tin
  - Thông báo lỗi và hướng dẫn rõ ràng

## Cài đặt

1. Clone repository:
```bash
git clone <repository-url>
cd mvp-2
```

2. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

3. Tạo file `.env` và thêm các API key cần thiết:
```
OMDB_API_KEY=your_omdb_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

## Sử dụng

1. Chạy chương trình:
```bash
cd scripts
python main.py
```

2. Nhập tên phim cần tìm (tiếng Việt hoặc tiếng Anh)
3. Chọn phim từ danh sách kết quả
4. Xem thông tin chi tiết và phân tích
5. Nhấn Enter để tiếp tục tìm kiếm hoặc 'q' để thoát

## Lưu ý

- Cần có API key của OMDb và OpenAI để sử dụng đầy đủ tính năng
- Thời gian phân tích có thể mất vài giây do phải gọi API
- Nếu tìm kiếm bằng tiếng Việt không có kết quả, chương trình sẽ tự động thử tìm bằng tiếng Anh
- Đảm bảo kết nối internet ổn định để có trải nghiệm tốt nhất 