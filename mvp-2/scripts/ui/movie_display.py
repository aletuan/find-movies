from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from api import openai_helper
from config import UI_ICONS, UI_SEPARATOR

console = Console()

def display_movie_info(movie_details):
    """Display formatted movie information and AI analysis."""
    if not movie_details:
        console.print("[red]Không thể lấy thông tin chi tiết của phim.[/red]")
        return
    
    # Format basic information
    title = f"{UI_ICONS['movie']} {movie_details['Title']} ({movie_details['Year']})"
    basic_info = f"""
{UI_ICONS['duration']} Thời lượng: {movie_details['Runtime']}
{UI_ICONS['genre']} Thể loại: {movie_details['Genre']}
{UI_ICONS['director']} Đạo diễn: {movie_details['Director']}
{UI_ICONS['cast']} Diễn viên: {movie_details['Actors']}
"""
    
    # Display basic information
    console.print(Panel(f"{title}\n{basic_info}", border_style="blue"))
    
    # Display ratings
    if movie_details.get('Ratings'):
        table = Table(title="ĐÁNH GIÁ")
        table.add_column("Nguồn", justify="right", style="cyan")
        table.add_column("Điểm", style="magenta")
        
        for rating in movie_details['Ratings']:
            table.add_row(rating['Source'], rating['Value'])
        console.print(table)
    
    # Display awards if available
    from utils.awards_parser import parse_awards
    if movie_details.get('Awards') and movie_details['Awards'] != 'N/A':
        awards_panel = parse_awards(movie_details['Awards'])
        console.print(Panel(awards_panel, title=f"{UI_ICONS['award']} GIẢI THƯỞNG", border_style="yellow"))
    
    # Get and display AI analysis
    console.print(f"\n{UI_ICONS['review']} PHÂN TÍCH VÀ ĐÁNH GIÁ:")
    analysis_result = openai_helper.get_movie_analysis(movie_details)
    if isinstance(analysis_result, str) and not analysis_result.startswith("Error"):
        wrapped_text = "\n".join([line.strip() for line in analysis_result.split("\n") if line.strip()])
        console.print(Panel(wrapped_text, border_style="green", width=100))
    else:
        console.print(f"[red]{analysis_result}[/red]")
    
    # Show poster if available
    if movie_details.get('Poster') and movie_details['Poster'] != 'N/A':
        console.print(f"\n{UI_ICONS['poster']} Poster: {movie_details['Poster']}")
    
    console.print("\n" + UI_SEPARATOR)

def display_search_results(movies, movie_details_list):
    """Display search results in a table format."""
    table = Table(title="KẾT QUẢ TÌM KIẾM")
    table.add_column("#", justify="right", style="cyan", no_wrap=True)
    table.add_column("Tên phim", style="magenta")
    table.add_column("Năm", style="green", justify="center")
    table.add_column("IMDb Rating", style="yellow", justify="center")
    table.add_column("Số đánh giá", style="blue", justify="right")
    table.add_column("Box Office", style="green", justify="right")
    table.add_column("Giải thưởng", style="yellow")
    table.add_column("IMDb ID", style="dim")
    
    for i, (movie, details) in enumerate(zip(movies[:10], movie_details_list), 1):
        # Format the votes number with commas
        votes = details.get('imdbVotes', 'N/A')
        if votes != 'N/A':
            votes = "{:,}".format(int(votes.replace(',', '')))
        
        # Format box office value
        box_office = details.get('BoxOffice', 'N/A')
        if box_office != 'N/A':
            try:
                box_office_value = int(box_office.replace('$', '').replace(',', ''))
                box_office = f"${box_office_value:,}"
            except ValueError:
                box_office = 'N/A'
        
        # Format awards information
        awards = details.get('Awards', 'N/A')
        if awards != 'N/A' and len(awards) > 30:
            awards = awards[:27] + "..."
        
        table.add_row(
            str(i),
            movie.get('Title', 'N/A'),
            movie.get('Year', 'N/A'),
            details.get('imdbRating', 'N/A'),
            votes,
            box_office,
            awards,
            movie.get('imdbID', 'N/A')
        )
    
    return table 