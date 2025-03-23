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
        awards_text = movie_details['Awards']
        formatted_awards = []
        
        # Extract Oscar nominations/wins
        if 'Oscar' in awards_text:
            oscar_part = awards_text.split('.')[0]
            formatted_awards.append(f"🏆 Oscar: {oscar_part}")
        
        # Extract total wins and nominations
        wins_noms = awards_text.split('.')[-1].strip()
        if wins_noms:
            wins_count = 0
            noms_count = 0
            
            # Extract wins
            if 'wins' in wins_noms:
                wins_part = wins_noms.split('&')[0].strip()
                try:
                    wins_count = int(''.join(filter(str.isdigit, wins_part)))
                    formatted_awards.append(f"🌟 Giải thưởng đã thắng: {wins_count}")
                except ValueError:
                    pass
            
            # Extract nominations
            if 'nominations' in wins_noms:
                noms_part = wins_noms.split('&')[1].strip() if '&' in wins_noms else wins_noms
                try:
                    noms_count = int(''.join(filter(str.isdigit, noms_part)))
                    formatted_awards.append(f"🎯 Đề cử: {noms_count}")
                except ValueError:
                    pass
        
        awards_panel = "\n".join(formatted_awards) if formatted_awards else awards_text
        console.print(Panel(awards_panel, title=f"{UI_ICONS['award']} GIẢI THƯỞNG", border_style="yellow"))
    
    # Get and display AI analysis
    console.print(f"\n{UI_ICONS['review']} PHÂN TÍCH VÀ ĐÁNH GIÁ:")
    analysis_result = openai_helper.get_movie_analysis(movie_details)
    if isinstance(analysis_result, str) and not analysis_result.startswith("Error"):
        # Wrap text at 90 characters and create a panel
        wrapped_text = "\n".join([line.strip() for line in analysis_result.split("\n") if line.strip()])
        console.print(Panel(wrapped_text, border_style="green", width=100))
    else:
        console.print(f"[red]{analysis_result}[/red]")
    
    # Show poster if available
    if movie_details.get('Poster') and movie_details['Poster'] != 'N/A':
        console.print(f"\n{UI_ICONS['poster']} Poster: {movie_details['Poster']}")
    
    console.print("\n" + UI_SEPARATOR)

def sort_movies_by_year(movies):
    """Sort movies by year in descending order (newest first)."""
    def extract_year(movie):
        try:
            year_str = movie.get('Year', '0')
            # Handle TV series with year ranges (e.g., "2020–2023")
            if '–' in year_str:
                year_str = year_str.split('–')[0]
            return int(year_str) if year_str.isdigit() else 0
        except (ValueError, TypeError):
            return 0
    
    return sorted(movies, key=extract_year, reverse=True)

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
        
        # Sort movies by year (newest first)
        movies = sort_movies_by_year(movies)
        
        # Display search results
        if movies:
            table = Table(title="KẾT QUẢ TÌM KIẾM")
            table.add_column("#", justify="right", style="cyan", no_wrap=True)
            table.add_column("Tên phim", style="magenta")
            table.add_column("Năm", style="green", justify="center")
            table.add_column("IMDb Rating", style="yellow", justify="center")
            table.add_column("Số đánh giá", style="blue", justify="right")
            table.add_column("Box Office", style="green", justify="right")
            table.add_column("Giải thưởng", style="yellow")
            table.add_column("IMDb ID", style="dim")
            
            console.print("\nĐang lấy thông tin chi tiết cho các phim...")
            for i, movie in enumerate(movies[:10], 1):
                # Get detailed info for each movie to get rating and votes
                movie_details = omdb.get_movie_details(movie.get('imdbID'))
                
                # Format the votes number with commas
                votes = movie_details.get('imdbVotes', 'N/A')
                if votes != 'N/A':
                    votes = "{:,}".format(int(votes.replace(',', '')))
                
                # Format box office value
                box_office = movie_details.get('BoxOffice', 'N/A')
                if box_office != 'N/A':
                    # Remove '$' and ',' then format with commas
                    try:
                        box_office_value = int(box_office.replace('$', '').replace(',', ''))
                        box_office = f"${box_office_value:,}"
                    except ValueError:
                        box_office = 'N/A'
                
                # Format awards information
                awards = movie_details.get('Awards', 'N/A')
                if awards != 'N/A':
                    # Shorten awards text if too long
                    if len(awards) > 30:
                        awards = awards[:27] + "..."
                
                table.add_row(
                    str(i),
                    movie.get('Title', 'N/A'),
                    movie.get('Year', 'N/A'),
                    movie_details.get('imdbRating', 'N/A'),
                    votes,
                    box_office,
                    awards,
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