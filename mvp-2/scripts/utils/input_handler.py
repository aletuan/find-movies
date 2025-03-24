#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Input handler module for the Movie Search Script.
Handles user input validation and processing.
"""

def get_movie_title():
    """Get and validate movie title input.
    
    Returns:
        str: Valid movie title or None to quit
    """
    while True:
        title = input("\nNhập tên phim (hoặc 'q' để thoát): ").strip()
        
        if title.lower() == 'q':
            return None
            
        if not title:
            print("[red]Vui lòng nhập tên phim.[/red]")
            continue
            
        if len(title) < 2:
            print("[red]Tên phim phải có ít nhất 2 ký tự.[/red]")
            continue
            
        if title.isdigit():
            print("[red]Tên phim không thể chỉ chứa số.[/red]")
            continue
            
        return title

def get_movie_selection(max_movies):
    """Get and validate user's movie selection.
    
    Args:
        max_movies (int): Maximum number of movies to choose from
        
    Returns:
        int: Selected movie index (0-based) or -1 to go back
    """
    while True:
        choice = input("\nChọn số để xem chi tiết (hoặc 'b' để quay lại): ").strip().lower()
        
        if choice == 'b':
            return -1
            
        try:
            num = int(choice)
            if 1 <= num <= max_movies:
                return num - 1  # Convert to 0-based index
            else:
                print(f"Vui lòng chọn số từ 1 đến {max_movies}.")
        except ValueError:
            print("Vui lòng nhập một số hợp lệ hoặc 'b' để quay lại.") 