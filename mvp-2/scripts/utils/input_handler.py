def get_movie_selection(max_items):
    """Handle movie selection input."""
    while True:
        try:
            selection = input("\nChọn số để xem chi tiết (hoặc 'b' để quay lại): ")
            
            if selection.lower() == 'b':
                return 'back'
            
            idx = int(selection) - 1
            if 0 <= idx < max_items:
                return idx
            else:
                print("Lựa chọn không hợp lệ. Vui lòng thử lại.")
        except ValueError:
            print("Vui lòng nhập một số hợp lệ.") 