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

def get_movie_analysis(movie_data):
    """Get movie analysis and review using OpenAI.
    
    Args:
        movie_data (dict): Movie details from OMDb API
        
    Returns:
        dict: Analysis results containing summary and review
    """
    if not check_api_key():
        return {
            "success": False,
            "error": "OpenAI API key not configured"
        }
    
    try:
        # Prepare movie information for the prompt
        movie_info = f"""
Tên phim: {movie_data.get('Title')}
Năm: {movie_data.get('Year')}
Đạo diễn: {movie_data.get('Director')}
Diễn viên: {movie_data.get('Actors')}
Thể loại: {movie_data.get('Genre')}
Điểm IMDb: {movie_data.get('imdbRating')}
Nội dung: {movie_data.get('Plot')}
Giải thưởng: {movie_data.get('Awards')}
"""

        # Create prompt for analysis
        prompt = f"""Là một nhà phê bình phim chuyên nghiệp, hãy phân tích và đánh giá bộ phim sau bằng tiếng Việt:

{movie_info}

Yêu cầu:
1. Tóm tắt nội dung chính của phim (2-3 đoạn)
2. Phân tích các điểm mạnh và điểm yếu về:
   - Kịch bản
   - Diễn xuất
   - Đạo diễn
   - Hình ảnh và âm thanh
3. Đánh giá tổng thể và đề xuất đối tượng khán giả phù hợp

Hãy viết với giọng điệu chuyên nghiệp nhưng dễ hiểu, tránh spoiler quan trọng."""

        # Get completion from OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Bạn là một nhà phê bình phim chuyên nghiệp."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        analysis = response.choices[0].message['content']
        
        return {
            "success": True,
            "analysis": analysis
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error getting movie analysis: {str(e)}"
        }

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