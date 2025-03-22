#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TMDb API module for the Movie Search Script.
Handles API calls to The Movie Database (TMDb).
"""

import requests
import sys
import os

# Add parent directory to sys.path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import TMDB_API_KEY, TMDB_BASE_URL, LANGUAGE

def search_movie(query):
    """Search for movies by title.
    
    Args:
        query (str): Movie title to search for
        
    Returns:
        list: List of movie results
    """
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
    """Get detailed information about a movie.
    
    Args:
        movie_id (int): TMDb movie ID
        
    Returns:
        dict: Movie details or None if request fails
    """
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
    """Get cast and crew information for a movie.
    
    Args:
        movie_id (int): TMDb movie ID
        
    Returns:
        dict: Movie credits or None if request fails
    """
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

def get_movie_reviews(movie_id, limit=3):
    """Get user reviews for a movie.
    
    Args:
        movie_id (int): TMDb movie ID
        limit (int, optional): Maximum number of reviews to return
        
    Returns:
        list: List of reviews
    """
    url = f"{TMDB_BASE_URL}/movie/{movie_id}/reviews"
    params = {
        "api_key": TMDB_API_KEY,
        "language": LANGUAGE,
        "page": 1
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        results = response.json().get("results", [])
        return results[:limit]  # Return only the specified number of reviews
    except requests.exceptions.RequestException as e:
        print(f"Error getting movie reviews: {e}")
        return []

def check_api_key():
    """Check if the TMDb API key is valid.
    
    Returns:
        bool: True if API key is valid, False otherwise
    """
    if TMDB_API_KEY == "YOUR_TMDB_API_KEY" or not TMDB_API_KEY:
        print("Lỗi: Vui lòng thiết lập TMDB API KEY trong config.py.")
        print("Bạn có thể đăng ký API key tại: https://www.themoviedb.org/settings/api")
        return False
    return True

def extract_movie_data(movie_details):
    """Extract relevant data from movie details.
    
    Args:
        movie_details (dict): Full movie details from TMDb API
        
    Returns:
        dict: Simplified movie data
    """
    if not movie_details:
        return {}
    
    # Extract basic information
    data = {
        "title": movie_details.get("title", "Không có tên"),
        "original_title": movie_details.get("original_title", ""),
        "release_date": movie_details.get("release_date", ""),
        "release_year": movie_details.get("release_date", "")[:4] if movie_details.get("release_date") else None,
        "runtime": movie_details.get("runtime", 0),
        "overview": movie_details.get("overview", "Không có mô tả"),
        "vote_average": movie_details.get("vote_average", 0),
        "vote_count": movie_details.get("vote_count", 0),
        "poster_path": movie_details.get("poster_path", ""),
    }
    
    # Extract genres
    data["genres"] = []
    for genre in movie_details.get("genres", []):
        data["genres"].append(genre.get("name", ""))
    
    # Extract production companies
    data["production_companies"] = []
    for company in movie_details.get("production_companies", []):
        data["production_companies"].append(company.get("name", ""))
    
    # Extract directors and cast
    data["directors"] = []
    data["cast"] = []
    credits = movie_details.get("credits", {})
    
    for crew_member in credits.get("crew", []):
        if crew_member.get("job") == "Director":
            data["directors"].append(crew_member.get("name", ""))
    
    for cast_member in credits.get("cast", [])[:5]:  # Get top 5 cast members
        data["cast"].append(cast_member.get("name", ""))
    
    return data 