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