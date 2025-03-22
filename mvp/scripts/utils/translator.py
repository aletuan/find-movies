#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Translator module for the Movie Search Script.
Handles translations to Vietnamese and other text processing functions.
"""

from googletrans import Translator
import sys
import os

# Add parent directory to sys.path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import TARGET_LANGUAGE

# Initialize translator
translator = Translator()

def translate_to_vietnamese(text):
    """Translate text to Vietnamese.
    
    Args:
        text (str): Text to translate
        
    Returns:
        str: Translated text or original text if translation fails
    """
    if not text:
        return ""
    try:
        translation = translator.translate(text, dest=TARGET_LANGUAGE)
        return translation.text
    except Exception as e:
        print(f"Translation error: {e}")
        return text

def translate_texts(texts_list):
    """Translate a list of texts to Vietnamese.
    
    Args:
        texts_list (list): List of texts to translate
        
    Returns:
        list: List of translated texts
    """
    return [translate_to_vietnamese(text) for text in texts_list] 