#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Movie Search Script
------------------
This script allows users to search for movie information by title and displays detailed
information in Vietnamese. It uses TMDB API for movie data and translates results.
"""

import sys

# Import modules
from config import UI_SEPARATOR, UI_ICONS, TMDB_IMAGE_BASE_URL
from api import tmdb, omdb, youtube, wikipedia
from utils.translator import translate_to_vietnamese, translate_texts
from utils.formatter import format_date, format_rating_source, format_runtime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def display_movie_info(movie):
    """Display formatted movie information in Vietnamese."""
    # Get full movie details
    movie_details = tmdb.get_movie_details(movie["id"])
    if not movie_details:
        print("Không thể lấy thông tin chi tiết của phim.")
        return
    
    # Extract movie data
    movie_data = tmdb.extract_movie_data(movie_details)
    
    # Get external ratings and details from OMDb
    omdb_ratings, imdb_id = omdb.get_omdb_ratings(
        movie_data["title"], 
        movie_data["release_year"]
    )
    
    # Get detailed info from OMDb including plot
    omdb_details = omdb.get_omdb_details(
        movie_data["title"],
        movie_data["release_year"]
    )
    
    # Get YouTube reviews
    youtube_reviews = youtube.get_youtube_reviews(movie_data["title"], movie_data["release_year"])
    
    # Generate YouTube search URL
    youtube_search_url = youtube.get_youtube_search_url(movie_data["title"], movie_data["release_year"])
    
    # Get Wikipedia plot
    wiki_plot_data = wikipedia.get_movie_plot(movie_data["title"], movie_data["release_year"])
    
    # Get user reviews from TMDb
    reviews = tmdb.get_movie_reviews(movie["id"], limit=2)
    
    # Translate information to Vietnamese
    title_vi = translate_to_vietnamese(movie_data["title"]) if movie_data["title"] != movie_data["original_title"] else movie_data["title"]
    original_title_vi = f" ({movie_data['original_title']})" if movie_data["original_title"] and movie_data["original_title"] != movie_data["title"] else ""
    overview_vi = translate_to_vietnamese(movie_data["overview"])
    genres_vi = translate_texts(movie_data["genres"])
    production_companies_vi = translate_texts(movie_data["production_companies"])
    
    # Translate IMDb plot if available
    imdb_plot_vi = ""
    if omdb_details['success'] and omdb_details['plot']:
        imdb_plot_vi = translate_to_vietnamese(omdb_details['plot'])
    
    # Translate Wikipedia plot if it's in English
    wiki_plot_vi = ""
    if wiki_plot_data['success']:
        if wiki_plot_data['language'] == 'en':
            wiki_plot_vi = translate_to_vietnamese(wiki_plot_data['plot'])
        else:
            wiki_plot_vi = wiki_plot_data['plot']
    
    # Format date and runtime
    formatted_release_date = format_date(movie_data["release_date"])
    hours, minutes = format_runtime(movie_data["runtime"])
    
    # Format and display information using Rich
    movie_title = f"{UI_ICONS['movie']} {title_vi}{original_title_vi}"
    basic_info = f"""
{UI_ICONS['date']} Ngày phát hành: {formatted_release_date}
{UI_ICONS['duration']} Thời lượng: {hours}h {minutes}m
{UI_ICONS['genre']} Thể loại: {', '.join(genres_vi)}
{UI_ICONS['director']} Đạo diễn: {', '.join(movie_data['directors'])}
{UI_ICONS['cast']} Diễn viên chính: {', '.join(movie_data['cast'])}
{UI_ICONS['company']} Hãng sản xuất: {', '.join(production_companies_vi)}
"""
    console.print(Panel(basic_info, title=movie_title, border_style="blue"))

    # Display ratings using a table
    if omdb_details['success'] and omdb_details['ratings']:
        table = Table(title="ĐÁNH GIÁ")
        table.add_column("Nguồn", justify="right", style="cyan", no_wrap=True)
        table.add_column("Điểm", style="magenta")
        table.add_row("The Movie Database", f"{movie_data['vote_average']}/10 (dựa trên {movie_data['vote_count']} lượt đánh giá)")
        for rating in omdb_details['ratings']:
            source = format_rating_source(rating.get("Source", ""))
            value = rating.get("Value", "N/A")
            table.add_row(source, value)
        console.print(table)

    # Display awards if available
    if omdb_details['success'] and omdb_details['awards']:
        awards_vi = translate_to_vietnamese(omdb_details['awards'])
        console.print(Panel(awards_vi, title="GIẢI THƯỞNG", border_style="yellow"))

    # Display summary
    console.print(Panel(overview_vi, title="TÓM TẮT NỘI DUNG PHIM (The Movie Database)", border_style="green"))
    if omdb_details['success'] and imdb_plot_vi:
        console.print(Panel(imdb_plot_vi, title="TÓM TẮT NỘI DUNG PHIM (Internet Movie Database)", border_style="green"))
    if wiki_plot_data['success']:
        console.print(Panel(wiki_plot_vi, title="TÓM TẮT CỐT TRUYỆN (WIKIPEDIA)", border_style="green"))

    # Display YouTube reviews using Rich Table
    console.print(f"\n{UI_ICONS['youtube']} VIDEOS TRÊN YOUTUBE:")
    if youtube_reviews:
        table = Table(title="VIDEO REVIEW")
        table.add_column("#", justify="right", style="cyan", no_wrap=True)
        table.add_column("Tiêu đề", style="magenta")
        table.add_column("Kênh", style="green")
        table.add_column("Ngày xuất bản", style="yellow")
        for i, review in enumerate(youtube_reviews, 1):
            published_date = review['published_at'] if review['published_at'] else "N/A"
            table.add_row(str(i), review['title'], review['channel'], published_date)
        console.print(table)
        console.print(f"\nXem thêm: {youtube_search_url}")
    else:
        console.print(f"Tìm kiếm trên YouTube: {youtube_search_url}")

    # Display poster URL if available
    if movie_data["poster_path"]:
        poster_url = f"{TMDB_IMAGE_BASE_URL}{movie_data['poster_path']}"
        console.print(f"\n{UI_ICONS['poster']} Poster: {poster_url}")

    console.print("\n" + UI_SEPARATOR)

def main():
    """Main function to run the movie search script."""
    print("\n=== TÌM KIẾM THÔNG TIN PHIM ===\n")
    
    # Check API keys
    if not tmdb.check_api_key():
        sys.exit(1)
    
    omdb.check_api_key()
    youtube.check_api_key()
    
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
        movies = tmdb.search_movie(query)
        
        # Display search results using Rich Table
        if movies:
            table = Table(title="KẾT QUẢ TÌM KIẾM")
            table.add_column("#", justify="right", style="cyan", no_wrap=True)
            table.add_column("Tên phim", style="magenta")
            table.add_column("Năm phát hành", style="green")
            for i, movie in enumerate(movies[:10], 1):  # Show max 10 results
                release_year = movie.get("release_date", "")[:4] if movie.get("release_date") else "N/A"
                table.add_row(str(i), movie.get('title', 'N/A'), release_year)
            console.print(table)
        else:
            console.print("Không tìm thấy phim nào. Vui lòng thử lại với từ khóa khác.")
        
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