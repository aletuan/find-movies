from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

# Initialize Rich console
console = Console()

# UI Icons
UI_ICONS = {
    'movie': '🎬',
    'date': '📅',
    'duration': '⏱️',
    'genre': '🎭',
    'director': '🎯',
    'cast': '👥',
    'company': '🏢',
    'rating': '⭐',
    'award': '🏆',
    'review': '📝',
    'summary': '📖',
    'youtube': '🎥',
    'poster': '🖼️',
    'search': '🔍',
    'error': '❌',
    'success': '✅'
}

# UI Separator
UI_SEPARATOR = "=" * 80

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