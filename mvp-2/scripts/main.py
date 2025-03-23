#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Movie Search and Analysis Script
------------------------------
This script allows users to search for movie information and get AI-powered analysis.
It uses OMDb API for movie data and OpenAI for analysis.
"""

import sys
from rich.console import Console

from api import omdb, openai_helper
from ui.movie_display import display_movie_info, display_search_results
from utils.movie_processor import sort_movies_by_year, get_movie_details_batch
from utils.input_handler import get_movie_selection

console = Console()

def main():
    """Main function to run the movie search script."""
    print("\n=== TÌM KIẾM VÀ PHÂN TÍCH PHIM ===\n")
    
    # Check API keys
    if not omdb.check_api_key():
        sys.exit(1)
    openai_helper.check_api_key()
    
    while True:
        # Get movie title from user
        query = input("\nNhập tên phim (hoặc 'q' để thoát): ").strip()
        
        if query.lower() in ['q', 'quit', 'exit']:
            print("\nCảm ơn bạn đã sử dụng chương trình. Tạm biệt!")
            break
        
        if not query:
            print("Vui lòng nhập tên phim.")
            continue
        
        print(f"\nĐang tìm kiếm phim '{query}'...")
        
        # Search for movies
        movies = omdb.search_movies(query)
        
        # Display search results
        if movies:
            # Sort movies by year and get details
            movies = sort_movies_by_year(movies)
            console.print("\nĐang lấy thông tin chi tiết cho các phim...")
            movie_details_list = get_movie_details_batch(movies, omdb)
            
            # Display results table
            table = display_search_results(movies, movie_details_list)
            console.print(table)
            
            # Let user select a movie
            selection = get_movie_selection(len(movies[:10]))
            if selection == 'back':
                continue
            
            # Display selected movie details
            display_movie_info(movie_details_list[selection])
            input("\nNhấn Enter để tiếp tục...")
        else:
            console.print("[red]Không tìm thấy phim nào. Vui lòng thử lại với từ khóa khác.[/red]")

if __name__ == "__main__":
    main() 