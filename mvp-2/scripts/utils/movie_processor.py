def sort_movies_by_year(movies):
    """Sort movies by year in descending order (newest first)."""
    def extract_year(movie):
        try:
            year_str = movie.get('Year', '0')
            # Handle TV series with year ranges (e.g., "2020–2023")
            if '–' in year_str:
                year_str = year_str.split('–')[0]
            return int(year_str) if year_str.isdigit() else 0
        except (ValueError, TypeError):
            return 0
    
    return sorted(movies, key=extract_year, reverse=True)

def get_movie_details_batch(movies, omdb_client):
    """Get movie details for a batch of movies."""
    return [omdb_client.get_movie_details(m['imdbID']) for m in movies[:10]] 