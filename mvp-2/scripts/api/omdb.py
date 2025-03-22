#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OMDb API module for the Movie Search Script.
Handles API calls to OMDb for movie information.
"""

import requests
import sys
import os

# Add parent directory to sys.path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import OMDB_API_KEY, OMDB_BASE_URL

def search_movies(title):
    """Search for movies by title using the OMDb API.
    
    Args:
        title (str): The movie title to search for
        
    Returns:
        list: List of movie search results
    """
    if not check_api_key():
        return []
        
    params = {
        "apikey": OMDB_API_KEY,
        "s": title,
        "type": "movie"
    }
    
    try:
        response = requests.get(OMDB_BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data.get("Response") == "True":
            return data.get("Search", [])
        return []
        
    except requests.exceptions.RequestException as e:
        print(f"Error searching movies: {e}")
        return []

def get_movie_details(imdb_id):
    """Get detailed movie information by IMDb ID.
    
    Args:
        imdb_id (str): The IMDb ID of the movie
        
    Returns:
        dict: Movie details or None if not found
    """
    if not check_api_key():
        return None
        
    params = {
        "apikey": OMDB_API_KEY,
        "i": imdb_id,
        "plot": "full"
    }
    
    try:
        response = requests.get(OMDB_BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data.get("Response") == "True":
            return data
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"Error getting movie details: {e}")
        return None

def check_api_key():
    """Check if the OMDb API key is valid.
    
    Returns:
        bool: True if API key is valid, False otherwise
    """
    if not OMDB_API_KEY or OMDB_API_KEY == "YOUR_OMDB_API_KEY":
        print("Cảnh báo: OMDb API KEY chưa được cài đặt.")
        print("Tìm kiếm phim sẽ không khả dụng.")
        print("Bạn có thể đăng ký API key tại: http://www.omdbapi.com/apikey.aspx")
        print("Tiếp tục mà không có tìm kiếm phim...\n")
        return False
    return True 