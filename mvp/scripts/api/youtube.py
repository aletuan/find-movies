#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
YouTube API module for the Movie Search Script.
Handles API calls to YouTube and transcript extraction.
"""

import requests
import urllib.parse
import re
import nltk
import sys
import os
from nltk.tokenize import sent_tokenize
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

# Add parent directory to sys.path to import config and utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import YOUTUBE_API_KEY, YOUTUBE_API_URL, DEFAULT_SEARCH_SUFFIX, YOUTUBE_RESULT_LIMIT
from utils.formatter import clean_transcript_text, extract_video_id
from utils.translator import translate_to_vietnamese

# Download necessary NLTK data if not already available
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

def get_youtube_reviews(movie_title, year=None, limit=None, custom_keywords=None):
    """Search for movie reviews on YouTube.
    
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
    if YOUTUBE_API_KEY == "YOUR_YOUTUBE_API_KEY" or not YOUTUBE_API_KEY:
        return []
    
    # Prepare search query
    if custom_keywords:
        # Use custom keywords with movie title
        search_query = f"{movie_title} {custom_keywords}"
    else:
        # Default search query
        search_query = f"{movie_title} {DEFAULT_SEARCH_SUFFIX}"
    
    # Prepare API request
    params = {
        "key": YOUTUBE_API_KEY,
        "q": search_query,
        "part": "snippet",
        "type": "video",
        "maxResults": limit,
        "relevanceLanguage": "vi"
    }
    
    try:
        response = requests.get(YOUTUBE_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for item in data.get("items", []):
            video_id = item.get("id", {}).get("videoId", "")
            title = item.get("snippet", {}).get("title", "")
            channel = item.get("snippet", {}).get("channelTitle", "")
            published_at = item.get("snippet", {}).get("publishedAt", "")
            thumbnail = item.get("snippet", {}).get("thumbnails", {}).get("medium", {}).get("url", "")
            
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
    except Exception as e:
        print(f"Error searching YouTube: {e}")
        return []

def get_youtube_search_url(movie_title, year=None, custom_keywords=None):
    """Generate YouTube search URL for a movie.
    
    Args:
        movie_title (str): Movie title
        year (str, optional): Release year
        custom_keywords (str, optional): Custom search keywords
        
    Returns:
        str: YouTube search URL
    """
    if custom_keywords:
        search_query = f"{movie_title} {custom_keywords}"
    else:
        search_query = f"{movie_title} {DEFAULT_SEARCH_SUFFIX}"
    
    encoded_query = urllib.parse.quote(search_query)
    return f"https://www.youtube.com/results?search_query={encoded_query}"

def get_youtube_transcript(video_id, translate=True):
    """Get transcript (subtitles) from a YouTube video and optionally translate it to Vietnamese.
    
    Args:
        video_id (str): YouTube video ID
        translate (bool, optional): Whether to translate transcript to Vietnamese
        
    Returns:
        dict: Contains 'success' (bool), 'transcript' (str), and 'summary' (str)
    """
    result = {
        'success': False,
        'transcript': '',
        'summary': ''
    }
    
    try:
        # Try to get available transcripts
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # First try to get Vietnamese transcript if translate is True
        if translate:
            try:
                transcript = transcript_list.find_transcript(['vi'])
                transcript_data = transcript.fetch()
            except:
                # If Vietnamese transcript doesn't exist, get any transcript and translate
                try:
                    transcript = transcript_list.find_transcript(['en'])
                    transcript_data = transcript.fetch()
                except:
                    # Get any available transcript
                    transcript = transcript_list.find_generated_transcript(['en'])
                    transcript_data = transcript.fetch()
        else:
            # Get any available transcript
            try:
                transcript = transcript_list.find_transcript(['en'])
                transcript_data = transcript.fetch()
            except:
                transcript = transcript_list.find_generated_transcript(['en'])
                transcript_data = transcript.fetch()
        
        # Format transcript data to plain text
        formatter = TextFormatter()
        transcript_text = formatter.format_transcript(transcript_data)
        
        # Clean transcript text
        transcript_text = clean_transcript_text(transcript_text)
        
        # Generate summary of transcript (first 200 characters + first 3 sentences)
        preview = transcript_text[:200] + "..."
        sentences = sent_tokenize(transcript_text)
        first_sentences = ' '.join(sentences[:3]) if len(sentences) > 3 else transcript_text
        
        # Translate if needed
        if translate:
            try:
                preview = translate_to_vietnamese(preview)
                first_sentences = translate_to_vietnamese(first_sentences)
            except:
                # If translation fails, keep original
                pass
        
        result['success'] = True
        result['transcript'] = transcript_text
        result['preview'] = preview
        result['summary'] = first_sentences
        
    except Exception as e:
        result['summary'] = f"Không thể lấy phụ đề của video: {str(e)}"
        
    return result

def check_api_key():
    """Check if the YouTube API key is valid.
    
    Returns:
        bool: True if API key is valid, False otherwise
    """
    if YOUTUBE_API_KEY == "YOUR_YOUTUBE_API_KEY" or not YOUTUBE_API_KEY:
        print("Cảnh báo: YouTube API KEY chưa được cài đặt.")
        print("Tìm kiếm đánh giá phim trên YouTube sẽ không khả dụng.")
        print("Bạn có thể đăng ký API key tại: https://console.cloud.google.com/apis/library/youtube.googleapis.com")
        print("Tiếp tục mà không có tìm kiếm YouTube nâng cao...\n")
        return False
    return True 