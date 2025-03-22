#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Translator module for the Movie Search Script.
Handles translations to Vietnamese and other text processing functions.
"""

import sys
import os
import time
import json

# Add parent directory to sys.path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import TARGET_LANGUAGE

# Initialize translator with retry logic
try:
    from googletrans import Translator
    translator = Translator(service_urls=['translate.google.com'])
except Exception as e:
    print(f"Error initializing translator: {e}")
    translator = None

def translate_to_vietnamese(text):
    """Translate text to Vietnamese with robust error handling.
    
    Args:
        text (str): Text to translate
        
    Returns:
        str: Translated text or original text if translation fails
    """
    if text is None or text == "":
        return ""
    
    if translator is None:
        return text
    
    # Maximum retry attempts
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # Add a small delay between retries to avoid rate limiting
            if retry_count > 0:
                time.sleep(1)
                
            translation = translator.translate(text, dest='vi')
            
            # Verify we have valid translated text
            if translation and hasattr(translation, 'text') and translation.text:
                return translation.text
            else:
                # If translate returned None or empty, return original
                return text
                
        except json.JSONDecodeError as e:
            # Specific handling for JSON decode errors
            print(f"JSON error in translation: {e}")
            retry_count += 1
            if retry_count >= max_retries:
                return text
                
        except Exception as e:
            print(f"Translation error: {e}")
            return text
    
    # If all retries failed, return original text
    return text

def translate_texts(texts_list):
    """Translate a list of texts to Vietnamese.
    
    Args:
        texts_list (list): List of texts to translate
        
    Returns:
        list: List of translated texts
    """
    if texts_list is None:
        return []
        
    result = []
    for text in texts_list:
        try:
            translated = translate_to_vietnamese(text)
            result.append(translated)
        except Exception as e:
            print(f"Error translating list item: {e}")
            result.append(text)  # Use original if translation fails
            
    return result 