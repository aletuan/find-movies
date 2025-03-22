#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration file for the Movie Search Script.
Contains API keys, URLs, and other constants.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(dotenv_path)

# API keys (from environment variables)
TMDB_API_KEY = os.getenv("TMDB_API_KEY")  # TMDB API key
OMDB_API_KEY = os.getenv("OMDB_API_KEY")  # OMDb API key
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")  # YouTube API key

# Base URLs
TMDB_BASE_URL = "https://api.themoviedb.org/3"
OMDB_BASE_URL = "http://www.omdbapi.com/"
YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/search"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

# Language settings
LANGUAGE = os.getenv("LANGUAGE", "en-US")
TARGET_LANGUAGE = os.getenv("TARGET_LANGUAGE", "vi")  # Vietnamese

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