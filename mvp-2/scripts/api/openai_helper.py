#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OpenAI API module for the Movie Search Script.
Handles API calls to OpenAI for movie analysis and reviews.
"""

import sys
import os
from openai import OpenAI

# Add parent directory to sys.path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import OPENAI_API_KEY

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def get_movie_analysis(movie_details):
    """Get movie analysis and review using OpenAI.
    
    Args:
        movie_details (dict): Movie details from OMDb API
        
    Returns:
        str: Analysis results containing summary and review
    """
    if not OPENAI_API_KEY:
        return "Error: OpenAI API key not found"

    try:
        prompt = f"""Hãy viết một bài phân tích chuyên sâu về bộ phim "{movie_details['Title']}" với độ dài khoảng 10-15 câu.

        Bài phân tích cần đảm bảo các nội dung sau một cách tự nhiên và liền mạch:
        - Giới thiệu về bối cảnh ra đời và vị trí của phim trong dòng phim cùng thể loại
        - Tóm tắt nội dung chính và các chủ đề của phim mà không tiết lộ các tình tiết quan trọng
        - Phân tích về kịch bản, cách phát triển nhân vật và thông điệp của phim
        - Đánh giá về diễn xuất, phong cách đạo diễn, hình ảnh và âm thanh
        - Kết luận về giá trị tổng thể và đối tượng khán giả phù hợp

        Thông tin tham khảo:
        - Đạo diễn: {movie_details.get('Director', 'Không có thông tin')}
        - Diễn viên: {movie_details.get('Actors', 'Không có thông tin')}
        - Thể loại: {movie_details.get('Genre', 'Không có thông tin')}
        - Điểm IMDb: {movie_details.get('imdbRating', 'Không có thông tin')}
        - Giải thưởng: {movie_details.get('Awards', 'Không có thông tin')}
        
        Hãy viết với giọng điệu chuyên nghiệp, khách quan nhưng dễ hiểu, tránh chia thành các mục riêng biệt. Các ý cần được kết nối tự nhiên, tạo một bài phân tích mạch lạc và có chiều sâu."""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional film critic who writes flowing, insightful, and cohesive reviews in Vietnamese. Your reviews seamlessly blend analysis of different aspects while maintaining clarity and depth."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error getting movie analysis: {str(e)}"

def get_awards_analysis(movie_details):
    """Get detailed analysis of movie awards using OpenAI.
    
    Args:
        movie_details (dict): Movie details from OMDb API
        
    Returns:
        dict: Structured awards analysis
    """
    if not OPENAI_API_KEY:
        return {"error": "OpenAI API key not found"}

    try:
        prompt = f"""Phân tích chi tiết các giải thưởng của bộ phim sau và trả về kết quả có cấu trúc:

Thông tin giải thưởng: {movie_details.get('Awards', 'Không có thông tin')}

Hãy phân tích và trả về kết quả theo định dạng JSON với cấu trúc sau:
{{
    "oscar_awards": [
        {{
            "category": "Tên hạng mục",
            "result": "Thắng/Đề cử",
            "year": "Năm"
        }}
    ],
    "golden_globe_awards": [...],
    "bafta_awards": [...],
    "other_major_awards": [
        {{
            "award_name": "Tên giải thưởng",
            "category": "Hạng mục",
            "result": "Thắng/Đề cử",
            "year": "Năm"
        }}
    ],
    "total_wins": số_giải_thắng,
    "total_nominations": số_đề_cử,
    "summary": "Tóm tắt ngắn gọn về thành tựu giải thưởng nổi bật nhất"
}}

Chỉ trả về JSON, không kèm theo bất kỳ văn bản nào khác."""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a movie awards analyst who provides structured analysis of film awards in Vietnamese."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        
        try:
            import json
            return json.loads(response.choices[0].message.content.strip())
        except json.JSONDecodeError:
            return {"error": "Could not parse awards analysis"}
            
    except Exception as e:
        return {"error": f"Error analyzing awards: {str(e)}"}

def check_api_key():
    """Check if the OpenAI API key is valid.
    
    Returns:
        bool: True if API key is valid, False otherwise
    """
    if not OPENAI_API_KEY or OPENAI_API_KEY == "YOUR_OPENAI_API_KEY":
        print("Cảnh báo: OpenAI API KEY chưa được cài đặt.")
        print("Phân tích phim bằng AI sẽ không khả dụng.")
        print("Bạn có thể đăng ký API key tại: https://platform.openai.com/")
        print("Tiếp tục mà không có phân tích AI...\n")
        return False
    return True 