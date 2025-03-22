#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration file for the Movie Search Script.
Contains API keys, URLs, and other constants.
"""

import os
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(dotenv_path)

# API keys
OMDB_API_KEY = os.getenv("OMDB_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Base URLs
OMDB_BASE_URL = "http://www.omdbapi.com/"

# Initialize Rich console
console = Console()

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
    "poster": "🖼️",
    "award": "🏆"
}

def create_movie_panel(title, content):
    """Create a rich panel for displaying movie information."""
    return Panel(
        Text(content, style="white"),
        title=title,
        border_style="blue"
    )

def create_rating_table(ratings):
    """Create a rich table for displaying ratings."""
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Nguồn")
    table.add_column("Điểm")
    
    for source, value in ratings.items():
        table.add_row(source, value)
    
    return table 