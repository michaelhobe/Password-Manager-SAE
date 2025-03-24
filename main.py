# Main launcher file
import tkinter as tk
from password_manager_gui import RetrowavePasswordManagerGUI
import pygame
import os

def main():
    # Initialize pygame mixer for audio
    pygame.mixer.init()
    
    # Get the path to the music file in the same directory as this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    music_file = os.path.join(script_dir, "templehymn.mp3")  # Change to your music filename
    
    # Check if the music file exists
    if os.path.exists(music_file):
        try:
            # Load and play music
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.set_volume(0.5)  # 50% volume
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely
            print(f"Playing music: {music_file}")
        except Exception as e:
            print(f"Error playing music: {e}")
    else:
        print(f"Music file not found: {music_file}")
    
    # Create the main window
    root = tk.Tk()
    
    # Create the app
    app = RetrowavePasswordManagerGUI(root)
    
    # Add music control functionality
    def toggle_music():
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            music_button.config(text="PLAY MUSIC")
        else:
            pygame.mixer.music.unpause()
            music_button.config(text="PAUSE MUSIC")
    
    # Create button frame for the music control
    music_frame = tk.Frame(root, bg="#000100")
    music_frame.pack(side=tk.BOTTOM, fill=tk.X, before=app.status_bar)
    
    # Add music control button
    button_style = {
        'relief': 'raised',
        'borderwidth': 2,
        'bg': '#303060',
        'fg': '#10ffff',
        'activebackground': '#505050',
        'activeforeground': '#ff00ff',
        'font': ('Arial', 10, 'bold'),
        'width': 15,
        'height': 10
    }
    
    music_button = tk.Button(music_frame, text="PAUSE MUSIC", command=toggle_music, **button_style)
    music_button.pack(pady=5)
    
    # Set up cleanup when the window is closed
    def on_closing():
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start the main event loop
    root.mainloop()

# Run the application when this file is executed directly
if __name__ == "__main__":
    main()