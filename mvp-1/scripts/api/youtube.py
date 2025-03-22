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
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

# Add parent directory to sys.path to import config and utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import YOUTUBE_API_KEY, YOUTUBE_API_URL, DEFAULT_SEARCH_SUFFIX, YOUTUBE_RESULT_LIMIT

def is_vietnamese_channel(channel_title):
    """Check if a YouTube channel is likely Vietnamese based on its title.
    
    Args:
        channel_title (str): The title of the YouTube channel
        
    Returns:
        bool: True if the channel appears to be Vietnamese
    """
    # List of common Vietnamese words/patterns in channel names
    vn_patterns = [
        'review', 'phim', 'điện ảnh', 'phê phim', 'xem phim',
        'việt', 'viet', 'vn', '.vn', 'vietnam',
        'phim hay', 'phim mới', 'phim chiếu rạp',
        'cine', 'cinema', 'rap', 'rạp'
    ]
    
    # Convert to lowercase for case-insensitive matching
    channel_lower = channel_title.lower()
    
    # Check for Vietnamese diacritical marks
    vietnamese_chars = 'àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ'
    has_vietnamese_chars = any(c in vietnamese_chars for c in channel_lower)
    
    # Check for Vietnamese patterns
    has_vn_pattern = any(pattern.lower() in channel_lower for pattern in vn_patterns)
    
    return has_vietnamese_chars or has_vn_pattern

def contains_movie_title(video_title, movie_title):
    """Check if a video title contains the movie title.
    
    Args:
        video_title (str): The title of the YouTube video
        movie_title (str): The title of the movie being searched
        
    Returns:
        bool: True if the video title contains the movie title
    """
    # Convert both to lowercase for case-insensitive matching
    video_lower = video_title.lower()
    movie_lower = movie_title.lower()
    
    # Remove common special characters from movie title
    movie_clean = ''.join(c for c in movie_lower if c.isalnum() or c.isspace())
    
    # Split movie title into words
    movie_words = movie_clean.split()
    
    # For single word titles, check if it exists as a whole word
    if len(movie_words) == 1:
        import re
        pattern = r'\b' + re.escape(movie_clean) + r'\b'
        return bool(re.search(pattern, video_lower))
    
    # For multi-word titles, check if all words are present in order
    current_pos = 0
    for word in movie_words:
        pos = video_lower.find(word, current_pos)
        if pos == -1:
            return False
        current_pos = pos + len(word)
    
    return True

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
    
    # Set up API request with a higher maxResults to account for filtering
    params = {
        "key": YOUTUBE_API_KEY,
        "q": query,
        "part": "snippet",
        "type": "video",
        "maxResults": min(50, limit * 3),  # Request more results to filter
        "relevanceLanguage": "vi"
    }
    
    try:
        # Make API request
        response = requests.get(YOUTUBE_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Process and filter results
        results = []
        for item in data.get("items", []):
            video_id = item.get("id", {}).get("videoId", "")
            snippet = item.get("snippet", {})
            title = snippet.get("title", "")
            channel = snippet.get("channelTitle", "")
            published_at = snippet.get("publishedAt", "")
            thumbnail = snippet.get("thumbnails", {}).get("medium", {}).get("url", "")
            
            # Only include videos from Vietnamese channels that contain the movie title
            if (video_id and title and 
                is_vietnamese_channel(channel) and 
                contains_movie_title(title, movie_title)):
                
                results.append({
                    "title": title,
                    "channel": channel,
                    "url": f"https://www.youtube.com/watch?v={video_id}",
                    "published_at": published_at[:10] if published_at else "",  # Just get the date part
                    "thumbnail": thumbnail,
                    "video_id": video_id
                })
                
                # Break if we have enough Vietnamese results
                if len(results) >= limit:
                    break
                
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

def get_video_transcript(video_id):
    """Get transcript (subtitles) from a YouTube video.
    
    Args:
        video_id (str): YouTube video ID
        
    Returns:
        dict: Dictionary containing success status and transcript data
            - success (bool): Whether transcript was retrieved successfully
            - transcript (list): List of transcript segments with text and timestamps
            - error (str): Error message if any
    """
    try:
        # Try to get Vietnamese transcript first
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        try:
            # Try to get Vietnamese transcript
            transcript = transcript_list.find_transcript(['vi'])
        except NoTranscriptFound:
            try:
                # If Vietnamese not available, get English and translate
                transcript = transcript_list.find_transcript(['en'])
                transcript = transcript.translate('vi')
            except NoTranscriptFound:
                # If no English transcript, get auto-generated and translate
                transcript = transcript_list.find_generated_transcript(['en'])
                transcript = transcript.translate('vi')
        
        # Get the actual transcript data
        transcript_data = transcript.fetch()
        
        return {
            "success": True,
            "transcript": transcript_data,
            "error": None
        }
        
    except TranscriptsDisabled:
        return {
            "success": False,
            "transcript": None,
            "error": "Phụ đề đã bị tắt cho video này."
        }
    except Exception as e:
        return {
            "success": False,
            "transcript": None,
            "error": f"Không thể lấy phụ đề: {str(e)}"
        } 