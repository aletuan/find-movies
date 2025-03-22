#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Movie Search Script
------------------
This script allows users to search for movie information by title and displays detailed
information in Vietnamese. It uses TMDB API for movie data and translates results.
"""

import os
import sys
import requests
import json
from datetime import datetime
from googletrans import Translator

# API Configuration
TMDB_API_KEY = "12d8852faa36602d14b98d24eecc10de"  # Replace with your TMDB API key
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"
LANGUAGE = "en-US"

# Initialize translator
translator = Translator()

def translate_to_vietnamese(text):
    """Translate text to Vietnamese."""
    if not text:
        return ""
    try:
        translation = translator.translate(text, dest="vi")
        return translation.text
    except Exception as e:
        print(f"Translation error: {e}")
        return text

def search_movie(query):
    """Search for movies by title."""
    url = f"{TMDB_BASE_URL}/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "language": LANGUAGE,
        "query": query,
        "page": 1,
        "include_adult": False
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()["results"]
    except requests.exceptions.RequestException as e:
        print(f"Error searching for movie: {e}")
        return []

def get_movie_details(movie_id):
    """Get detailed information about a movie."""
    url = f"{TMDB_BASE_URL}/movie/{movie_id}"
    params = {
        "api_key": TMDB_API_KEY,
        "language": LANGUAGE,
        "append_to_response": "credits,reviews"
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting movie details: {e}")
        return None

def get_movie_credits(movie_id):
    """Get cast and crew information for a movie."""
    url = f"{TMDB_BASE_URL}/movie/{movie_id}/credits"
    params = {
        "api_key": TMDB_API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting movie credits: {e}")
        return None

def format_date(date_str):
    """Format date string to Vietnamese format."""
    if not date_str:
        return "Không có thông tin"
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%d/%m/%Y")
    except ValueError:
        return date_str

def display_movie_info(movie):
    """Display formatted movie information in Vietnamese."""
    # Get full movie details
    movie_details = get_movie_details(movie["id"])
    if not movie_details:
        print("Không thể lấy thông tin chi tiết của phim.")
        return
    
    # Basic information
    title = movie_details.get("title", "Không có tên")
    original_title = movie_details.get("original_title", "")
    release_date = format_date(movie_details.get("release_date", ""))
    runtime = movie_details.get("runtime", 0)
    
    # Production companies
    production_companies = []
    for company in movie_details.get("production_companies", []):
        production_companies.append(company.get("name", ""))
    
    # Genres
    genres = []
    for genre in movie_details.get("genres", []):
        genres.append(genre.get("name", ""))
    
    # Overview/Plot
    overview = movie_details.get("overview", "Không có mô tả")
    
    # Ratings
    vote_average = movie_details.get("vote_average", 0)
    vote_count = movie_details.get("vote_count", 0)
    
    # Directors and top cast members
    directors = []
    cast = []
    credits = movie_details.get("credits", {})
    
    for crew_member in credits.get("crew", []):
        if crew_member.get("job") == "Director":
            directors.append(crew_member.get("name", ""))
    
    for cast_member in credits.get("cast", [])[:5]:  # Get top 5 cast members
        cast.append(cast_member.get("name", ""))
    
    # Translate information to Vietnamese
    title_vi = translate_to_vietnamese(title) if title != original_title else title
    original_title_vi = f" ({original_title})" if original_title and original_title != title else ""
    overview_vi = translate_to_vietnamese(overview)
    genres_vi = [translate_to_vietnamese(genre) for genre in genres]
    production_companies_vi = [translate_to_vietnamese(company) for company in production_companies]
    
    # Format and display information
    print("\n" + "=" * 50)
    print(f"🎬 {title_vi}{original_title_vi}")
    print("=" * 50)
    
    print(f"\n📅 Ngày phát hành: {release_date}")
    if runtime:
        hours, minutes = divmod(runtime, 60)
        print(f"⏱️ Thời lượng: {hours}h {minutes}m")
    
    print(f"\n🎭 Thể loại: {', '.join(genres_vi)}")
    
    if directors:
        print(f"\n🎬 Đạo diễn: {', '.join(directors)}")
    
    if cast:
        print(f"\n🌟 Diễn viên chính: {', '.join(cast)}")
    
    if production_companies_vi:
        print(f"\n🏢 Hãng sản xuất: {', '.join(production_companies_vi)}")
    
    print(f"\n⭐ Đánh giá: {vote_average}/10 (dựa trên {vote_count} lượt đánh giá)")
    
    print(f"\n📝 Tóm tắt nội dung:\n{overview_vi}")
    
    # Display poster URL if available
    if movie_details.get("poster_path"):
        poster_url = f"{TMDB_IMAGE_BASE_URL}{movie_details['poster_path']}"
        print(f"\n🖼️ Poster: {poster_url}")
    
    print("\n" + "=" * 50)

def main():
    """Main function to run the movie search script."""
    print("\n=== TÌM KIẾM THÔNG TIN PHIM ===\n")
    
    # Check if API key is set
    if TMDB_API_KEY == "YOUR_TMDB_API_KEY":
        print("Lỗi: Vui lòng thiết lập TMDB API KEY trong script.")
        print("Bạn có thể đăng ký API key tại: https://www.themoviedb.org/settings/api")
        sys.exit(1)
    
    while True:
        # Get movie title from user
        query = input("\nNhập tên phim (hoặc 'q' để thoát): ")
        
        if query.lower() in ['q', 'quit', 'exit']:
            print("\nCảm ơn bạn đã sử dụng tìm kiếm phim. Tạm biệt!")
            break
        
        if not query.strip():
            print("Vui lòng nhập tên phim.")
            continue
        
        print(f"\nĐang tìm kiếm phim '{query}'...")
        
        # Search for movies
        movies = search_movie(query)
        
        if not movies:
            print("Không tìm thấy phim nào. Vui lòng thử lại với từ khóa khác.")
            continue
        
        # Display search results
        print(f"\nTìm thấy {len(movies)} kết quả:")
        for i, movie in enumerate(movies[:10], 1):  # Show max 10 results
            release_year = movie.get("release_date", "")[:4] if movie.get("release_date") else "N/A"
            print(f"{i}. {movie.get('title')} ({release_year})")
        
        # Let user select a movie
        while True:
            try:
                selection = input("\nChọn số để xem chi tiết (hoặc 'b' để quay lại): ")
                
                if selection.lower() == 'b':
                    break
                
                idx = int(selection) - 1
                if 0 <= idx < len(movies[:10]):
                    display_movie_info(movies[idx])
                    input("\nNhấn Enter để tiếp tục...")
                    break
                else:
                    print("Lựa chọn không hợp lệ. Vui lòng thử lại.")
            except ValueError:
                print("Vui lòng nhập một số hợp lệ.")

if __name__ == "__main__":
    main() 