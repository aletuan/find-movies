#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
YouTube API module for the Movie Search Script.
Handles API calls to YouTube for finding related videos.
"""

import requests
import urllib.parse
import sys
import os

# Add parent directory to sys.path to import config and utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import YOUTUBE_API_KEY, YOUTUBE_API_URL, DEFAULT_SEARCH_SUFFIX, YOUTUBE_RESULT_LIMIT

def get_youtube_reviews(movie_title, year=None, limit=None, custom_keywords=None):
    """Search for movie reviews on YouTube using the YouTube API.
    
    Args:
        movie_title (str): The title of the movie
        year (str, optional): Release year of the movie
        limit (int, optional): Maximum number of results to return
        custom_keywords (str, optional): Custom search keywords provided by user
        
    Returns:
        list: List of YouTube video information
    """
    # Set default limit if not specified
    if limit is None:
        limit = YOUTUBE_RESULT_LIMIT
        
    # If YouTube API key is not set, return empty list
    if not check_api_key():
        return []
    
    # Prepare search query
    query = f"{movie_title} {year} review phim" if year else f"{movie_title} review phim"
    query += f" {custom_keywords}" if custom_keywords else f" {DEFAULT_SEARCH_SUFFIX}"
    
    # Set up API request
    params = {
        "key": YOUTUBE_API_KEY,
        "q": query,
        "part": "snippet",
        "type": "video",
        "maxResults": limit,
        "relevanceLanguage": "vi"
    }
    
    try:
        # Make API request
        response = requests.get(YOUTUBE_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Process results
        results = []
        for item in data.get("items", []):
            video_id = item.get("id", {}).get("videoId", "")
            snippet = item.get("snippet", {})
            title = snippet.get("title", "")
            channel = snippet.get("channelTitle", "")
            published_at = snippet.get("publishedAt", "")
            thumbnail = snippet.get("thumbnails", {}).get("medium", {}).get("url", "")
            
            if video_id and title:
                results.append({
                    "title": title,
                    "channel": channel,
                    "url": f"https://www.youtube.com/watch?v={video_id}",
                    "published_at": published_at[:10] if published_at else "",  # Just get the date part
                    "thumbnail": thumbnail,
                    "video_id": video_id
                })
                
        return results
    except requests.exceptions.RequestException as e:
        print(f"Error searching YouTube: {e}")
        return []

def check_api_key():
    """Check if the YouTube API key is valid.
    
    Returns:
        bool: True if API key is valid, False otherwise
    """
    if not YOUTUBE_API_KEY or YOUTUBE_API_KEY == "YOUR_YOUTUBE_API_KEY":
        print("Cảnh báo: YouTube API KEY chưa được cài đặt.")
        print("Tìm kiếm đánh giá phim trên YouTube sẽ không khả dụng.")
        print("Bạn có thể đăng ký API key tại: https://console.cloud.google.com/apis/library/youtube.googleapis.com")
        print("Tiếp tục mà không có tìm kiếm YouTube nâng cao...\n")
        return False
    return True 