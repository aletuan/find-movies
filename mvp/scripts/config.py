#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration file for the Movie Search Script.
Contains API keys, URLs, and other constants.
"""

import os

# API keys
TMDB_API_KEY = "12d8852faa36602d14b98d24eecc10de"  # Replace with your TMDB API key
OMDB_API_KEY = "f7011e0e"  # Replace with your OMDb API key
YOUTUBE_API_KEY = "AIzaSyAEYuawmYGIOJNKZ2Ey8G8LLcdFzs-rDVE"  # Replace with your YouTube API key

# Base URLs
TMDB_BASE_URL = "https://api.themoviedb.org/3"
OMDB_BASE_URL = "http://www.omdbapi.com/"
YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/search"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

# Language settings
LANGUAGE = "en-US"
TARGET_LANGUAGE = "vi"  # Vietnamese

# UI symbols and formatting
UI_SEPARATOR = "=" * 60
UI_ICONS = {
    "movie": "🎬",
    "date": "📅",
    "duration": "⏱️",
    "genre": "🎭",
    "director": "🎬",
    "cast": "🌟",
    "company": "🏢",
    "rating": "⭐",
    "review": "📣",
    "summary": "📝",
    "transcript": "🔤",
    "youtube": "📺",
    "poster": "🖼️"
}

# YouTube search defaults
DEFAULT_SEARCH_SUFFIX = "review đánh giá phim"
YOUTUBE_RESULT_LIMIT = 10 