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
from utils.input_handler import get_movie_selection, get_movie_title
from utils.translator import translate_to_english

console = Console()

def search_movie(title):
    """Search for movies with translation fallback.
    
    Args:
        title (str): Movie title to search for
        
    Returns:
        tuple: (movies list, movie details list)
    """
    print(f"\nĐang tìm kiếm phim '{title}'...")
    
    # First try with original title
    movies = omdb.search_movies(title)
    
    # If no results, try translating to English
    if not movies:
        translated_title = translate_to_english(title)
        if translated_title != title:
            console.print(f"\n[yellow]Không tìm thấy kết quả. Thử tìm với tên tiếng Anh: '{translated_title}'[/yellow]")
            movies = omdb.search_movies(translated_title)
    
    if movies:
        print("\nĐang lấy thông tin chi tiết cho các phim...")
        movie_details_list = get_movie_details_batch(movies, omdb)
        return movies, movie_details_list
    else:
        return [], []

def main():
    """Main function to run the movie search script."""
    print("\n=== TÌM KIẾM VÀ PHÂN TÍCH PHIM ===\n")
    
    # Check API keys
    if not omdb.check_api_key():
        sys.exit(1)
    openai_helper.check_api_key()
    
    while True:
        # Get movie title from user with validation
        title = get_movie_title()
        if title is None:  # User wants to quit
            print("\nCảm ơn bạn đã sử dụng chương trình. Tạm biệt!")
            break
            
        # Search for movies
        movies, movie_details_list = search_movie(title)
        
        if not movies:
            console.print("[red]Không tìm thấy phim phù hợp.[/red]")
            continue
            
        # Display search results
        table = display_search_results(movies, movie_details_list)
        console.print(table)
        
        # Get user selection
        selection = get_movie_selection(len(movies))
        if selection == -1:
            continue
            
        # Display movie details
        display_movie_info(movie_details_list[selection])
        
        input("\nNhấn Enter để tiếp tục...")

if __name__ == "__main__":
    main() 