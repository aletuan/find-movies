#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Translator module for the Movie Search Script.
Handles translation of movie titles using OpenAI.
"""

import sys
import os

# Add parent directory to sys.path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.openai_helper import client

def translate_to_english(text):
    """Translate Vietnamese text to English using OpenAI.
    
    Args:
        text (str): Text to translate
        
    Returns:
        str: Translated text or original text if translation fails
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional translator specializing in movie titles. Translate the given Vietnamese movie title to English. Only return the translated title, nothing else."
                },
                {
                    "role": "user",
                    "content": f"Translate this movie title from Vietnamese to English: {text}"
                }
            ],
            temperature=0.3,
            max_tokens=100
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[red]Lỗi khi dịch tên phim: {str(e)}[/red]")
        return text  # Return original text if translation fails 