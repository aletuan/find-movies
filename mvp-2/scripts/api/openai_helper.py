#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OpenAI API module for the Movie Search Script.
Handles API calls to OpenAI for movie analysis and reviews.
"""

import sys
import os
import openai

# Add parent directory to sys.path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import OPENAI_API_KEY

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

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
        openai.api_key = OPENAI_API_KEY
        
        prompt = f"""Hãy viết một bài review ngắn gọn về bộ phim "{movie_details['Title']}" trong khoảng 5-10 câu.
        Bài review nên bao gồm:
        1. Một câu tóm tắt cốt truyện chính
        2. Điểm mạnh và điểm yếu nổi bật của phim
        3. Đánh giá tổng thể và đề xuất đối tượng khán giả phù hợp
        
        Thông tin tham khảo về phim:
        - Đạo diễn: {movie_details.get('Director', 'Không có thông tin')}
        - Diễn viên: {movie_details.get('Actors', 'Không có thông tin')}
        - Thể loại: {movie_details.get('Genre', 'Không có thông tin')}
        - Điểm IMDb: {movie_details.get('imdbRating', 'Không có thông tin')}
        - Giải thưởng: {movie_details.get('Awards', 'Không có thông tin')}
        
        Hãy viết bằng tiếng Việt, với giọng điệu tự nhiên và dễ hiểu."""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional movie critic who writes concise and insightful reviews in Vietnamese."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error getting movie analysis: {str(e)}"

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