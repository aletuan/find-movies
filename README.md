# find-movies

A Python application to search for movie information, including details like title, director, actors, ratings, and YouTube reviews, with output in Vietnamese.

## Setup

1. Clone the repository
2. Install the required dependencies:
   ```
   pip install -r mvp/scripts/requirements.txt
   ```
3. Create a `.env` file in the `mvp` directory based on the `.env.example` template
4. Add your API keys to the `.env` file:
   - TMDB API key (get from [The Movie Database](https://www.themoviedb.org/settings/api))
   - OMDb API key (get from [OMDb API](https://www.omdbapi.com/apikey.aspx))
   - YouTube API key (get from [Google Cloud Console](https://console.cloud.google.com/))

## Usage

Run the script from the project root:

```
python mvp/scripts/main.py
```

Follow the on-screen prompts to search for and view movie information.

## Security Notes

- Never commit your `.env` file containing API keys to version control
- The `.gitignore` file is configured to exclude `.env` files
- For team development, share the `.env.example` template without actual API keys
