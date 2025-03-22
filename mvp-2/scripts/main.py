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
from rich.panel import Panel
from rich.table import Table

from api import omdb, openai_helper
from config import UI_SEPARATOR, UI_ICONS

console = Console()

def display_movie_info(movie_details):
    """Display formatted movie information and AI analysis."""
    if not movie_details:
        console.print("[red]Không thể lấy thông tin chi tiết của phim.[/red]")
        return
    
    # Format basic information
    title = f"{UI_ICONS['movie']} {movie_details['Title']} ({movie_details['Year']})"
    basic_info = f"""
{UI_ICONS['duration']} Thời lượng: {movie_details['Runtime']}
{UI_ICONS['genre']} Thể loại: {movie_details['Genre']}
{UI_ICONS['director']} Đạo diễn: {movie_details['Director']}
{UI_ICONS['cast']} Diễn viên: {movie_details['Actors']}
"""
    
    # Display basic information
    console.print(Panel(f"{title}\n{basic_info}", border_style="blue"))
    
    # Display ratings
    if movie_details.get('Ratings'):
        table = Table(title="ĐÁNH GIÁ")
        table.add_column("Nguồn", justify="right", style="cyan")
        table.add_column("Điểm", style="magenta")
        
        for rating in movie_details['Ratings']:
            table.add_row(rating['Source'], rating['Value'])
        console.print(table)
    
    # Display awards if available
    if movie_details.get('Awards') and movie_details['Awards'] != 'N/A':
        console.print(Panel(movie_details['Awards'], title=f"{UI_ICONS['award']} GIẢI THƯỞNG", border_style="yellow"))
    
    # Get and display AI analysis
    console.print(f"\n{UI_ICONS['review']} PHÂN TÍCH VÀ ĐÁNH GIÁ:")
    analysis_result = openai_helper.get_movie_analysis(movie_details)
    
    if analysis_result['success']:
        console.print(Panel(analysis_result['analysis'], border_style="green"))
    else:
        console.print(f"[red]{analysis_result['error']}[/red]")
    
    # Display poster URL if available
    if movie_details.get('Poster') and movie_details['Poster'] != 'N/A':
        console.print(f"\n{UI_ICONS['poster']} Poster: {movie_details['Poster']}")
    
    console.print("\n" + UI_SEPARATOR)

def main():
    """Main function to run the movie search script."""
    print("\n=== TÌM KIẾM VÀ PHÂN TÍCH PHIM ===\n")
    
    # Check API keys
    if not omdb.check_api_key():
        sys.exit(1)
    openai_helper.check_api_key()
    
    while True:
        # Get movie title from user
        query = input("\nNhập tên phim (hoặc 'q' để thoát): ")
        
        if query.lower() in ['q', 'quit', 'exit']:
            print("\nCảm ơn bạn đã sử dụng chương trình. Tạm biệt!")
            break
        
        if not query.strip():
            print("Vui lòng nhập tên phim.")
            continue
        
        print(f"\nĐang tìm kiếm phim '{query}'...")
        
        # Search for movies
        movies = omdb.search_movies(query)
        
        # Display search results
        if movies:
            table = Table(title="KẾT QUẢ TÌM KIẾM")
            table.add_column("#", justify="right", style="cyan")
            table.add_column("Tên phim", style="magenta")
            table.add_column("Năm", style="green")
            table.add_column("IMDb ID", style="blue")
            
            for i, movie in enumerate(movies[:10], 1):
                table.add_row(
                    str(i),
                    movie.get('Title', 'N/A'),
                    movie.get('Year', 'N/A'),
                    movie.get('imdbID', 'N/A')
                )
            console.print(table)
            
            # Let user select a movie
            while True:
                try:
                    selection = input("\nChọn số để xem chi tiết (hoặc 'b' để quay lại): ")
                    
                    if selection.lower() == 'b':
                        break
                    
                    idx = int(selection) - 1
                    if 0 <= idx < len(movies[:10]):
                        # Get and display movie details
                        movie_details = omdb.get_movie_details(movies[idx]['imdbID'])
                        display_movie_info(movie_details)
                        input("\nNhấn Enter để tiếp tục...")
                        break
                    else:
                        print("Lựa chọn không hợp lệ. Vui lòng thử lại.")
                except ValueError:
                    print("Vui lòng nhập một số hợp lệ.")
        else:
            console.print("[red]Không tìm thấy phim nào. Vui lòng thử lại với từ khóa khác.[/red]")

if __name__ == "__main__":
    main() 