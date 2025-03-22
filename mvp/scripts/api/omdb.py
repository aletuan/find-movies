#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OMDb API module for the Movie Search Script.
Handles API calls to the Open Movie Database (OMDb).
"""

import requests
import sys
import os

# Add parent directory to sys.path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import OMDB_API_KEY, OMDB_BASE_URL

def get_omdb_ratings(title, year=None):
    """Get ratings from OMDb API (IMDb, Rotten Tomatoes, Metacritic).
    
    Args:
        title (str): Movie title
        year (str, optional): Release year
        
    Returns:
        tuple: Tuple of (ratings list, IMDb ID)
    """
    params = {
        "apikey": OMDB_API_KEY,
        "t": title,
        "type": "movie",
        "r": "json"
    }
    
    if year:
        params["y"] = year
        
    try:
        response = requests.get(OMDB_BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data.get("Response") == "True":
            return data.get("Ratings", []), data.get("imdbID", "")
        return [], ""
    except requests.exceptions.RequestException as e:
        print(f"Error getting OMDb data: {e}")
        return [], ""

def check_api_key():
    """Check if the OMDb API key is valid.
    
    Returns:
        bool: True if API key is valid, False otherwise
    """
    if OMDB_API_KEY == "your_omdb_api_key" or not OMDB_API_KEY:
        print("Cảnh báo: OMDb API KEY chưa được cài đặt.")
        print("Thông tin đánh giá chi tiết từ IMDb, Rotten Tomatoes và Metacritic sẽ không khả dụng.")
        print("Bạn có thể đăng ký API key tại: https://www.omdbapi.com/apikey.aspx")
        print("Tiếp tục mà không có thông tin đánh giá chi tiết...\n")
        return False
    return True 