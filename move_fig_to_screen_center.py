import matplotlib.pyplot as plt
import tkinter as tk

def move_fig_to_screen_center(fig):
    # Create a dummy window to get the screen dimensions
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()

    # Get the figure manager
    manager = plt.get_current_fig_manager()

    # Calculate position to center the window
    fig_width, fig_height = fig.get_size_inches() * fig.dpi  # Get figure dimensions in pixels
    x_pos = (screen_width - fig_width) // 2
    y_pos = (screen_height - fig_height) // 2

    # Adjust based on the GUI backend
    backend = plt.get_backend()
    # Move the window to the center
    if backend == "TkAgg":
        # For Tkinter-based backends
        manager.window.geometry(f"+{x_pos}+{y_pos}")
    elif backend in ["Qt5Agg", "QtAgg"]:
        # For Qt-based backends
        manager.window.move(int(x_pos), int(y_pos))
    elif backend == "WXAgg":
        # For WX-based backends
        manager.window.SetPosition((x_pos, y_pos))
    else:
        print(f"Backend {backend} not supported for window positioning.", file=sys.stderr)
