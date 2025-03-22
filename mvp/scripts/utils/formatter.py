#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Formatter module for the Movie Search Script.
Handles formatting and cleanup of data for display.
"""

from datetime import datetime
import re

def format_date(date_str):
    """Format date string to Vietnamese format (DD/MM/YYYY).
    
    Args:
        date_str (str): Date string in format YYYY-MM-DD
        
    Returns:
        str: Formatted date or "Không có thông tin" if invalid
    """
    if not date_str:
        return "Không có thông tin"
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%d/%m/%Y")
    except ValueError:
        return date_str

def format_rating_source(source):
    """Translate rating source names to shorter versions.
    
    Args:
        source (str): Original rating source name
        
    Returns:
        str: Simplified source name
    """
    sources = {
        "Internet Movie Database": "IMDb",
        "Rotten Tomatoes": "Rotten Tomatoes",
        "Metacritic": "Metacritic"
    }
    return sources.get(source, source)

def format_runtime(runtime_minutes):
    """Format runtime from minutes to hours and minutes.
    
    Args:
        runtime_minutes (int): Runtime in minutes
        
    Returns:
        tuple: Tuple of (hours, minutes)
    """
    if not runtime_minutes:
        return (0, 0)
    return divmod(runtime_minutes, 60)

def clean_transcript_text(text):
    """Clean transcript text by removing special markers and extra spaces.
    
    Args:
        text (str): Raw transcript text
        
    Returns:
        str: Cleaned transcript text
    """
    # Remove things like [Music], [Applause], etc.
    text = re.sub(r'\[.*?\]', '', text)  
    # Replace newlines with spaces
    text = re.sub(r'\n+', ' ', text)  
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)  
    return text

def extract_video_id(youtube_url):
    """Extract the video ID from a YouTube URL.
    
    Args:
        youtube_url (str): YouTube URL
        
    Returns:
        str or None: YouTube video ID if found, None otherwise
    """
    # Regular expressions to find YouTube video ID
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    
    youtube_match = re.match(youtube_regex, youtube_url)
    if youtube_match:
        return youtube_match.group(6)
    return None 