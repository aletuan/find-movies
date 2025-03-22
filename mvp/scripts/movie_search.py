#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Movie Search Script
------------------
This script allows users to search for movie information by title and displays detailed
information in Vietnamese. It uses TMDB API for movie data and translates results.
"""

import os
import sys
import requests
import json
from datetime import datetime
from googletrans import Translator
import urllib.parse
import re
import time
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords

# Download necessary NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

# API Configuration
TMDB_API_KEY = "12d8852faa36602d14b98d24eecc10de"  # Replace with your TMDB API key
OMDB_API_KEY = "f7011e0e"  # Replace with your OMDb API key
YOUTUBE_API_KEY = "AIzaSyAEYuawmYGIOJNKZ2Ey8G8LLcdFzs-rDVE"  # Replace with your YouTube API key
TMDB_BASE_URL = "https://api.themoviedb.org/3"
OMDB_BASE_URL = "http://www.omdbapi.com/"
YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/search"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"
LANGUAGE = "en-US"

# Initialize translator
translator = Translator()

def translate_to_vietnamese(text):
    """Translate text to Vietnamese."""
    if not text:
        return ""
    try:
        translation = translator.translate(text, dest="vi")
        return translation.text
    except Exception as e:
        print(f"Translation error: {e}")
        return text

def search_movie(query):
    """Search for movies by title."""
    url = f"{TMDB_BASE_URL}/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "language": LANGUAGE,
        "query": query,
        "page": 1,
        "include_adult": False
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()["results"]
    except requests.exceptions.RequestException as e:
        print(f"Error searching for movie: {e}")
        return []

def get_movie_details(movie_id):
    """Get detailed information about a movie."""
    url = f"{TMDB_BASE_URL}/movie/{movie_id}"
    params = {
        "api_key": TMDB_API_KEY,
        "language": LANGUAGE,
        "append_to_response": "credits,reviews"
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting movie details: {e}")
        return None

def get_movie_credits(movie_id):
    """Get cast and crew information for a movie."""
    url = f"{TMDB_BASE_URL}/movie/{movie_id}/credits"
    params = {
        "api_key": TMDB_API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting movie credits: {e}")
        return None

def get_omdb_ratings(title, year=None):
    """Get ratings from OMDb API (IMDb, Rotten Tomatoes, Metacritic)."""
    params = {
        "apikey": OMDB_API_KEY,
        "t": title,
        "type": "movie",
        "r": "json"
    }
    
    if year:
        params["y"] = year
        
    try:
        response = requests.get(OMDB_BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data.get("Response") == "True":
            return data.get("Ratings", []), data.get("imdbID", "")
        return [], ""
    except requests.exceptions.RequestException as e:
        print(f"Error getting OMDb data: {e}")
        return [], ""

def get_movie_reviews(movie_id, limit=3):
    """Get user reviews for a movie."""
    url = f"{TMDB_BASE_URL}/movie/{movie_id}/reviews"
    params = {
        "api_key": TMDB_API_KEY,
        "language": LANGUAGE,
        "page": 1
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        results = response.json().get("results", [])
        return results[:limit]  # Return only the first 'limit' reviews
    except requests.exceptions.RequestException as e:
        print(f"Error getting movie reviews: {e}")
        return []

def format_date(date_str):
    """Format date string to Vietnamese format."""
    if not date_str:
        return "Không có thông tin"
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%d/%m/%Y")
    except ValueError:
        return date_str

def format_rating_source(source):
    """Translate rating source names to Vietnamese."""
    sources = {
        "Internet Movie Database": "IMDb",
        "Rotten Tomatoes": "Rotten Tomatoes",
        "Metacritic": "Metacritic"
    }
    return sources.get(source, source)

def get_youtube_reviews(movie_title, year=None, limit=10, custom_keywords=None):
    """Search for movie reviews on YouTube.
    
    Args:
        movie_title (str): The title of the movie
        year (str, optional): Release year of the movie
        limit (int, optional): Maximum number of results to return
        custom_keywords (str, optional): Custom search keywords provided by user
        
    Returns:
        list: List of YouTube video information
    """
    # If YouTube API key is not set, return empty list
    if YOUTUBE_API_KEY == "YOUR_YOUTUBE_API_KEY":
        return []
    
    # Prepare search query
    if custom_keywords:
        # Use custom keywords with movie title
        search_query = f"{movie_title} {custom_keywords}"
    else:
        # Default search query
        search_query = f"{movie_title} review đánh giá phim"
    
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
                    "thumbnail": thumbnail
                })
                
        return results
    except Exception as e:
        print(f"Error searching YouTube: {e}")
        return []

def get_youtube_search_url(movie_title, year=None, custom_keywords=None):
    """Generate YouTube search URL for a movie."""
    if custom_keywords:
        search_query = f"{movie_title} {custom_keywords}"
    else:
        search_query = f"{movie_title} review đánh giá phim"
    
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
        
        # Clean transcript
        transcript_text = re.sub(r'\[.*?\]', '', transcript_text)  # Remove things like [Music], [Applause]
        transcript_text = re.sub(r'\n+', ' ', transcript_text)  # Replace newlines with spaces
        transcript_text = re.sub(r'\s+', ' ', transcript_text)  # Remove multiple spaces
        
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

def extract_video_id(youtube_url):
    """Extract the video ID from a YouTube URL."""
    # Regular expressions to find YouTube video ID
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    
    youtube_match = re.match(youtube_regex, youtube_url)
    if youtube_match:
        return youtube_match.group(6)
    return None

def display_movie_info(movie):
    """Display formatted movie information in Vietnamese."""
    # Get full movie details
    movie_details = get_movie_details(movie["id"])
    if not movie_details:
        print("Không thể lấy thông tin chi tiết của phim.")
        return
    
    # Basic information
    title = movie_details.get("title", "Không có tên")
    original_title = movie_details.get("original_title", "")
    release_date = movie_details.get("release_date", "")
    release_year = release_date[:4] if release_date else None
    formatted_release_date = format_date(release_date)
    runtime = movie_details.get("runtime", 0)
    
    # Production companies
    production_companies = []
    for company in movie_details.get("production_companies", []):
        production_companies.append(company.get("name", ""))
    
    # Genres
    genres = []
    for genre in movie_details.get("genres", []):
        genres.append(genre.get("name", ""))
    
    # Overview/Plot
    overview = movie_details.get("overview", "Không có mô tả")
    
    # TMDB Ratings
    vote_average = movie_details.get("vote_average", 0)
    vote_count = movie_details.get("vote_count", 0)
    
    # Get external ratings from OMDb
    omdb_ratings, imdb_id = get_omdb_ratings(title, release_year)
    
    # Get YouTube reviews if API key is set
    youtube_reviews = []
    # Không yêu cầu người dùng nhập từ khóa tìm kiếm nữa
    youtube_keywords = ""  # Để trống để sử dụng từ khóa mặc định
    
    if YOUTUBE_API_KEY != "YOUR_YOUTUBE_API_KEY":
        youtube_reviews = get_youtube_reviews(title, release_year, limit=10)
    
    # Always generate a YouTube search URL
    youtube_search_url = get_youtube_search_url(title, release_year)
    
    # Get transcript from first YouTube result if available
    youtube_transcript_result = None
    if youtube_reviews and len(youtube_reviews) > 0:
        first_video = youtube_reviews[0]
        video_id = extract_video_id(first_video['url'])
        if video_id:
            youtube_transcript_result = get_youtube_transcript(video_id)
    
    # Directors and top cast members
    directors = []
    cast = []
    credits = movie_details.get("credits", {})
    
    for crew_member in credits.get("crew", []):
        if crew_member.get("job") == "Director":
            directors.append(crew_member.get("name", ""))
    
    for cast_member in credits.get("cast", [])[:5]:  # Get top 5 cast members
        cast.append(cast_member.get("name", ""))
    
    # Get reviews
    reviews = get_movie_reviews(movie["id"], limit=2)
    
    # Translate information to Vietnamese
    title_vi = translate_to_vietnamese(title) if title != original_title else title
    original_title_vi = f" ({original_title})" if original_title and original_title != title else ""
    overview_vi = translate_to_vietnamese(overview)
    genres_vi = [translate_to_vietnamese(genre) for genre in genres]
    production_companies_vi = [translate_to_vietnamese(company) for company in production_companies]
    
    # Format and display information
    print("\n" + "=" * 60)
    print(f"🎬 {title_vi}{original_title_vi}")
    print("=" * 60)
    
    print(f"\n📅 Ngày phát hành: {formatted_release_date}")
    if runtime:
        hours, minutes = divmod(runtime, 60)
        print(f"⏱️ Thời lượng: {hours}h {minutes}m")
    
    print(f"\n🎭 Thể loại: {', '.join(genres_vi)}")
    
    if directors:
        print(f"\n🎬 Đạo diễn: {', '.join(directors)}")
    
    if cast:
        print(f"\n🌟 Diễn viên chính: {', '.join(cast)}")
    
    if production_companies_vi:
        print(f"\n🏢 Hãng sản xuất: {', '.join(production_companies_vi)}")
    
    # Display ratings
    print("\n⭐ ĐÁNH GIÁ:")
    print(f"   • TMDB: {vote_average}/10 (dựa trên {vote_count} lượt đánh giá)")
    
    if imdb_id:
        imdb_url = f"https://www.imdb.com/title/{imdb_id}"
        print(f"   • IMDb URL: {imdb_url}")
        
    if omdb_ratings:
        for rating in omdb_ratings:
            source = format_rating_source(rating.get("Source", ""))
            value = rating.get("Value", "N/A")
            print(f"   • {source}: {value}")
    
    # Display reviews if available
    if reviews:
        print(f"\n📣 ĐÁNH GIÁ TỪ NGƯỜI XEM ({len(reviews)}):")
        for i, review in enumerate(reviews, 1):
            author = review.get("author", "Ẩn danh")
            content = review.get("content", "")
            
            # Truncate review content if it's too long
            if len(content) > 200:
                content = content[:197] + "..."
                
            # Translate review content
            content_vi = translate_to_vietnamese(content)
            
            print(f"\n   Đánh giá #{i} - {author}:")
            print(f"   \"{content_vi}\"")
    
    # Display movie summary
    print(f"\n📝 TÓM TẮT NỘI DUNG PHIM:\n{overview_vi}")
    
    # Display YouTube transcript summary if available (after movie summary)
    if youtube_transcript_result and youtube_transcript_result['success']:
        print(f"\n🔤 TÓM TẮT NỘI DUNG VIDEO YOUTUBE:")
        print(f"   {youtube_transcript_result['summary']}")
    
    # Display YouTube reviews
    print("\n📺 VIDEOS TRÊN YOUTUBE:")
    print(f"   Từ khóa tìm kiếm mặc định: '{title} review đánh giá phim'")
        
    if youtube_reviews:
        print(f"\n   Tìm thấy {len(youtube_reviews)} video trên YouTube:")
        for i, review in enumerate(youtube_reviews, 1):
            published_date = f" ({review['published_at']})" if review['published_at'] else ""
            print(f"   {i}. {review['title']} - {review['channel']}{published_date}")
            print(f"      {review['url']}")
        
        print(f"\n   Xem thêm: {youtube_search_url}")
    else:
        print(f"   Tìm kiếm trên YouTube: {youtube_search_url}")
    
    # Display poster URL if available
    if movie_details.get("poster_path"):
        poster_url = f"{TMDB_IMAGE_BASE_URL}{movie_details['poster_path']}"
        print(f"\n🖼️ Poster: {poster_url}")
    
    print("\n" + "=" * 60)

def main():
    """Main function to run the movie search script."""
    print("\n=== TÌM KIẾM THÔNG TIN PHIM ===\n")
    
    # Check if API keys are set
    if TMDB_API_KEY == "YOUR_TMDB_API_KEY":
        print("Lỗi: Vui lòng thiết lập TMDB API KEY trong script.")
        print("Bạn có thể đăng ký API key tại: https://www.themoviedb.org/settings/api")
        sys.exit(1)
        
    if OMDB_API_KEY == "your_omdb_api_key":
        print("Cảnh báo: OMDb API KEY chưa được cài đặt.")
        print("Thông tin đánh giá chi tiết từ IMDb, Rotten Tomatoes và Metacritic sẽ không khả dụng.")
        print("Bạn có thể đăng ký API key tại: https://www.omdbapi.com/apikey.aspx")
        print("Tiếp tục mà không có thông tin đánh giá chi tiết...\n")
    
    if YOUTUBE_API_KEY == "YOUR_YOUTUBE_API_KEY":
        print("Cảnh báo: YouTube API KEY chưa được cài đặt.")
        print("Tìm kiếm đánh giá phim trên YouTube sẽ không khả dụng.")
        print("Bạn có thể đăng ký API key tại: https://console.cloud.google.com/apis/library/youtube.googleapis.com")
        print("Tiếp tục mà không có tìm kiếm YouTube nâng cao...\n")
    
    while True:
        # Get movie title from user
        query = input("\nNhập tên phim (hoặc 'q' để thoát): ")
        
        if query.lower() in ['q', 'quit', 'exit']:
            print("\nCảm ơn bạn đã sử dụng tìm kiếm phim. Tạm biệt!")
            break
        
        if not query.strip():
            print("Vui lòng nhập tên phim.")
            continue
        
        print(f"\nĐang tìm kiếm phim '{query}'...")
        
        # Search for movies
        movies = search_movie(query)
        
        if not movies:
            print("Không tìm thấy phim nào. Vui lòng thử lại với từ khóa khác.")
            continue
        
        # Display search results
        print(f"\nTìm thấy {len(movies)} kết quả:")
        for i, movie in enumerate(movies[:10], 1):  # Show max 10 results
            release_year = movie.get("release_date", "")[:4] if movie.get("release_date") else "N/A"
            print(f"{i}. {movie.get('title')} ({release_year})")
        
        # Let user select a movie
        while True:
            try:
                selection = input("\nChọn số để xem chi tiết (hoặc 'b' để quay lại): ")
                
                if selection.lower() == 'b':
                    break
                
                idx = int(selection) - 1
                if 0 <= idx < len(movies[:10]):
                    display_movie_info(movies[idx])
                    input("\nNhấn Enter để tiếp tục...")
                    break
                else:
                    print("Lựa chọn không hợp lệ. Vui lòng thử lại.")
            except ValueError:
                print("Vui lòng nhập một số hợp lệ.")

if __name__ == "__main__":
    main() 