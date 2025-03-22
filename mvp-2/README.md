# Movie Search (Beta Version)

Ứng dụng tìm kiếm thông tin phim sử dụng ChatGPT API để tổng hợp và hiển thị thông tin chi tiết về phim.

## Tính năng

- Tìm kiếm thông tin phim bằng tên
- Hiển thị thông tin chi tiết bao gồm:
  - Tên phim (tiếng Việt và tiếng Anh)
  - Năm phát hành
  - Thời lượng
  - Thể loại
  - Đạo diễn
  - Diễn viên chính
  - Hãng sản xuất
  - Đánh giá từ các nguồn
  - Giải thưởng
  - Tóm tắt nội dung
  - Link poster phim
- Hiển thị đánh giá từ:
  - Giới phê bình
  - Người xem
  - Video review trên YouTube
- Giao diện console đẹp mắt với Rich

## Cài đặt

1. Clone repository:
```bash
git clone <repository-url>
cd mvp-beta
```

2. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

3. Tạo file `.env` và thêm API key của OpenAI:
```
OPENAI_API_KEY=your_openai_api_key_here
```

## Sử dụng

1. Chạy chương trình:
```bash
cd scripts
python main.py
```

2. Nhập tên phim cần tìm kiếm
3. Xem kết quả hiển thị
4. Nhấn Enter để tiếp tục tìm kiếm hoặc 'q' để thoát

## Lưu ý

- Cần có API key của OpenAI để sử dụng
- Kết quả tìm kiếm được tổng hợp từ nhiều nguồn khác nhau
- Thời gian tìm kiếm có thể mất vài giây do phải gọi API 