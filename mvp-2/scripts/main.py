#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Movie Search Script (Beta Version)
--------------------------------
This script uses ChatGPT API to search and display detailed movie information in Vietnamese.
"""

import json
import sys
from config import console, UI_ICONS, UI_SEPARATOR, create_movie_panel, create_rating_table
from movie_ai import MovieAI

def display_movie_info(movie_data):
    """Display formatted movie information using Rich."""
    # Create main movie panel
    movie_title = f"{UI_ICONS['movie']} {movie_data['title_vi']}"
    if movie_data.get('title_en'):
        movie_title += f" ({movie_data['title_en']})"
    
    # Basic information
    basic_info = f"""
{UI_ICONS['date']} Ngày phát hành: {movie_data['release_year']}
{UI_ICONS['duration']} Thời lượng: {movie_data['duration']}
{UI_ICONS['genre']} Thể loại: {', '.join(movie_data['genres'])}
{UI_ICONS['director']} Đạo diễn: {movie_data['director']}
{UI_ICONS['cast']} Diễn viên chính: {', '.join(movie_data['cast'])}
{UI_ICONS['company']} Hãng sản xuất: {movie_data['production_company']}
"""
    
    # Display basic information
    console.print(create_movie_panel(movie_title, basic_info))
    
    # Display ratings
    if movie_data.get('ratings'):
        console.print(f"\n{UI_ICONS['rating']} ĐÁNH GIÁ:")
        console.print(create_rating_table(movie_data['ratings']))
    
    # Display awards
    if movie_data.get('awards'):
        console.print(f"\n{UI_ICONS['award']} GIẢI THƯỞNG:")
        console.print(Panel(movie_data['awards'], title="Giải thưởng", border_style="yellow"))
    
    # Display summary
    console.print(f"\n{UI_ICONS['summary']} TÓM TẮT NỘI DUNG PHIM:")
    console.print(Panel(movie_data['summary'], title="Nội dung", border_style="green"))
    
    # Display poster URL if available
    if movie_data.get('poster_url'):
        console.print(f"\n{UI_ICONS['poster']} Poster: {movie_data['poster_url']}")
    
    console.print("\n" + UI_SEPARATOR)

def main():
    """Main function to run the movie search script."""
    console.print("\n=== TÌM KIẾM THÔNG TIN PHIM (BETA) ===\n")
    
    # Initialize MovieAI
    movie_ai = MovieAI()
    
    while True:
        # Get movie title from user
        query = input("\nNhập tên phim (hoặc 'q' để thoát): ")
        
        if query.lower() in ['q', 'quit', 'exit']:
            console.print("\nCảm ơn bạn đã sử dụng tìm kiếm phim. Tạm biệt!")
            break
        
        if not query.strip():
            console.print("Vui lòng nhập tên phim.")
            continue
        
        console.print(f"\n{UI_ICONS['search']} Đang tìm kiếm thông tin về phim '{query}'...")
        
        # Search for movie information
        movie_data = movie_ai.search_movie(query)
        
        if isinstance(movie_data, dict) and movie_data.get('error'):
            console.print(f"{UI_ICONS['error']} Lỗi: {movie_data['error']}")
            continue
        
        try:
            # Parse JSON response
            movie_data = json.loads(movie_data)
            
            # Display movie information
            display_movie_info(movie_data)
            
            # Get and display reviews
            console.print(f"\n{UI_ICONS['review']} Đang tìm kiếm đánh giá...")
            reviews = movie_ai.get_movie_reviews(movie_data['title_en'], movie_data['release_year'])
            
            if isinstance(reviews, dict) and reviews.get('error'):
                console.print(f"{UI_ICONS['error']} Lỗi khi lấy đánh giá: {reviews['error']}")
            else:
                reviews_data = json.loads(reviews)
                if reviews_data.get('critic_reviews'):
                    console.print("\nĐánh giá từ giới phê bình:")
                    console.print(Panel(reviews_data['critic_reviews'], border_style="blue"))
                
                if reviews_data.get('user_reviews'):
                    console.print("\nĐánh giá từ người xem:")
                    console.print(Panel(reviews_data['user_reviews'], border_style="cyan"))
                
                if reviews_data.get('youtube_reviews'):
                    console.print(f"\n{UI_ICONS['youtube']} Video Review trên YouTube:")
                    for review in reviews_data['youtube_reviews']:
                        console.print(f"• {review['title']} - {review['url']}")
            
            input("\nNhấn Enter để tiếp tục...")
            
        except json.JSONDecodeError:
            console.print(f"{UI_ICONS['error']} Lỗi: Không thể xử lý dữ liệu trả về từ API")
        except Exception as e:
            console.print(f"{UI_ICONS['error']} Lỗi: {str(e)}")

if __name__ == "__main__":
    main() 