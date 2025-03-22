import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MovieAI:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = "gpt-3.5-turbo"
        
    def search_movie(self, query):
        """Search for movies using ChatGPT."""
        prompt = f"""
        Tìm kiếm thông tin về phim: {query}
        Hãy cung cấp thông tin chi tiết về phim này dưới dạng JSON với các trường sau:
        {{
            "title_vi": "Tên phim bằng tiếng Việt",
            "title_en": "Tên phim bằng tiếng Anh",
            "release_year": "Năm phát hành",
            "duration": "Thời lượng (ví dụ: 2h 30m)",
            "genres": ["Thể loại 1", "Thể loại 2"],
            "director": "Tên đạo diễn",
            "cast": ["Diễn viên 1", "Diễn viên 2"],
            "production_company": "Tên hãng sản xuất",
            "ratings": {{
                "IMDb": "X.X/10",
                "TMDB": "X.X/10"
            }},
            "awards": "Các giải thưởng (nếu có)",
            "summary": "Tóm tắt nội dung phim",
            "poster_url": "Link poster phim (nếu có)"
        }}
        
        Lưu ý:
        - Đảm bảo tất cả các trường đều có giá trị
        - Nếu không có thông tin cho một trường, sử dụng giá trị mặc định phù hợp
        - Đảm bảo JSON được định dạng đúng
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Bạn là một chuyên gia về phim ảnh, có khả năng tìm kiếm và tổng hợp thông tin phim một cách chính xác. Hãy luôn trả về dữ liệu dưới dạng JSON với đầy đủ các trường được yêu cầu."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            # Parse the response and return movie information
            return response.choices[0].message.content
            
        except Exception as e:
            return {"error": str(e)}
    
    def get_movie_reviews(self, movie_title, year):
        """Get movie reviews using ChatGPT."""
        prompt = f"""
        Tìm kiếm và tổng hợp các đánh giá về phim {movie_title} ({year}) từ các nguồn uy tín.
        Hãy cung cấp:
        1. Đánh giá chung từ giới phê bình
        2. Đánh giá từ người xem
        3. Các video review trên YouTube (nếu có)
        
        Hãy trả về thông tin dưới dạng JSON với các trường tương ứng.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Bạn là một chuyên gia phê bình phim, có khả năng phân tích và tổng hợp các đánh giá về phim."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return {"error": str(e)} 