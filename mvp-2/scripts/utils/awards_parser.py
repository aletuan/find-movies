def parse_awards(awards_text):
    """Parse and format awards information."""
    if not awards_text or awards_text == 'N/A':
        return None
        
    formatted_awards = []
    sections = [s.strip() for s in awards_text.split('.') if s.strip()]
    
    for section in sections:
        if 'Oscar' in section:
            if 'Nominated for' in section:
                # Extract Oscar nominations
                num = ''.join(filter(str.isdigit, section))
                categories = []
                if 'including' in section.lower():
                    cats = section.split('including')[-1].strip()
                    categories = [c.strip() for c in cats.split(',')]
                formatted_awards.append(f"🏆 [yellow]Oscar[/yellow]: Đề cử {num} giải" + 
                    (f"\n   Các hạng mục: {', '.join(categories)}" if categories else ""))
            elif 'Won' in section:
                # Extract Oscar wins
                num = ''.join(filter(str.isdigit, section))
                categories = []
                if 'including' in section.lower():
                    cats = section.split('including')[-1].strip()
                    categories = [c.strip() for c in cats.split(',')]
                formatted_awards.append(f"🏆 [gold1]Oscar[/gold1]: Thắng {num} giải" + 
                    (f"\n   Các hạng mục: {', '.join(categories)}" if categories else ""))
        
        # Extract BAFTA awards
        elif 'BAFTA' in section:
            formatted_awards.append(f"🎭 [blue]BAFTA[/blue]: {section}")
        
        # Extract Golden Globe awards
        elif 'Golden Globe' in section:
            formatted_awards.append(f"🌟 [yellow]Golden Globe[/yellow]: {section}")
        
        # Extract total wins and nominations
        elif 'wins' in section or 'nominations' in section:
            wins_count = 0
            noms_count = 0
            
            # Extract wins
            if 'wins' in section:
                wins_part = section.split('&')[0].strip()
                try:
                    wins_count = int(''.join(filter(str.isdigit, wins_part)))
                    formatted_awards.append(f"[green]Tổng số giải thưởng đã thắng[/green]: {wins_count}")
                except ValueError:
                    pass
            
            # Extract nominations
            if 'nominations' in section:
                noms_part = section.split('&')[1].strip() if '&' in section else section
                try:
                    noms_count = int(''.join(filter(str.isdigit, noms_part)))
                    formatted_awards.append(f"[yellow]Tổng số đề cử[/yellow]: {noms_count}")
                except ValueError:
                    pass
    
    return "\n".join(formatted_awards) if formatted_awards else awards_text 