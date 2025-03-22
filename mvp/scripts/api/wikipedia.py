#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wikipedia API module for the Movie Search Script.
Handles fetching plot summaries and other information from Wikipedia.
"""

import wikipediaapi
import sys
import os
import re

# Add parent directory to sys.path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import TARGET_LANGUAGE

# Initialize Wikipedia API with a custom user agent
user_agent = 'MovieSearchApp/1.0 (quangvu@example.com)'
wiki_wiki = wikipediaapi.Wikipedia(
    language=TARGET_LANGUAGE.split('-')[0],  # Use first part of language code (e.g., 'vi' from 'vi-VN')
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent=user_agent
)

# Also initialize English Wikipedia for fallback
wiki_en = wikipediaapi.Wikipedia(
    language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent=user_agent
)

def get_movie_plot(movie_title, year=None, fallback_to_english=True):
    """Get movie plot summary from Wikipedia.
    
    Args:
        movie_title (str): Movie title
        year (str, optional): Release year to help disambiguate
        fallback_to_english (bool): Whether to try English Wikipedia if target language fails
        
    Returns:
        dict: Dictionary with plot, source_url, and language
    """
    result = {
        'plot': '',
        'source_url': '',
        'language': TARGET_LANGUAGE.split('-')[0],
        'success': False
    }
    
    # Try with year for more specific search
    search_term = f"{movie_title} ({year})" if year else movie_title
    search_term_film = f"{movie_title} film" if not year else f"{movie_title} film {year}"
    
    # Try different search terms
    search_terms = [
        search_term,
        search_term_film,
        movie_title  # Simplest form as last resort
    ]
    
    # Try each search term in target language
    for term in search_terms:
        page = wiki_wiki.page(term)
        if page.exists():
            result = extract_plot_from_page(page, result)
            if result['success']:
                return result
    
    # If all failed and fallback is enabled, try English Wikipedia
    if fallback_to_english:
        result['language'] = 'en'
        for term in search_terms:
            page = wiki_en.page(term)
            if page.exists():
                result = extract_plot_from_page(page, result)
                if result['success']:
                    return result
    
    # If we still don't have a plot, return empty result
    return result

def extract_plot_from_page(page, result):
    """Extract plot section from Wikipedia page.
    
    Args:
        page: Wikipedia page object
        result: Result dictionary to update
        
    Returns:
        dict: Updated result dictionary
    """
    # List of section titles that might contain plot information
    plot_section_titles = [
        'Plot', 'Synopsis', 'Story', 'Storyline', 'Summary', 'Plot summary',
        'Cốt truyện', 'Nội dung', 'Tóm tắt', 'Mô tả'
    ]
    
    # Check if any of the plot sections exist
    for section_title in plot_section_titles:
        if section_title in page.sections:
            section = page.sections[section_title]
            plot_text = section.text.strip()
            
            # If we found content, return it
            if plot_text:
                result['plot'] = plot_text
                result['source_url'] = page.fullurl
                result['success'] = True
                return result
    
    # If no dedicated plot section, try to extract from summary
    # Sometimes the first part of the article contains the plot
    summary = page.summary
    if summary and len(summary) > 200:  # Ensure it's substantial
        result['plot'] = summary
        result['source_url'] = page.fullurl
        result['success'] = True
        return result
    
    # If that fails, check if the content contains any plot information
    content = page.text
    if content:
        # Try to find plot-related paragraphs in the content
        paragraphs = content.split('\n\n')
        relevant_paragraphs = []
        
        # Look for paragraphs that might be plot descriptions
        for para in paragraphs:
            # Skip very short paragraphs
            if len(para) < 100:
                continue
                
            # Look for paragraphs that contain narrative phrases
            narrative_indicators = ['story', 'follows', 'centers', 'depicts', 'portrays', 
                                   'begins', 'ends', 'character', 'protagonist']
            
            # For Vietnamese
            if result['language'] == 'vi':
                narrative_indicators.extend(['kể về', 'tả về', 'mô tả', 'khởi đầu', 'kết thúc', 'nhân vật'])
                
            if any(indicator in para.lower() for indicator in narrative_indicators):
                relevant_paragraphs.append(para)
        
        # If we found relevant paragraphs, use them
        if relevant_paragraphs:
            result['plot'] = '\n\n'.join(relevant_paragraphs[:3])  # Limit to first 3 paragraphs
            result['source_url'] = page.fullurl
            result['success'] = True
            
    return result 