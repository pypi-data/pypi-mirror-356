import tkinter as tk
from PIL import ImageTk, Image
import time
import os
import sys
import subprocess

def launch_gui():
    print("[*] Launching GUI...")

    # Handles both normal and PyInstaller _MEIPASS environments
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

    # 👇 Use the correct path to gui.py (same folder as splash.py)
    gui_script = os.path.join(base_path, "gui.py")

    try:
        subprocess.call([sys.executable, gui_script])
    except Exception as e:
        print(f"[!] Failed to launch GUI: {e}")

def show_splash():
    splash = tk.Tk()
    splash.title("Welcome to AnujScan")
    splash.overrideredirect(True)
    splash.config(bg="#111111")

    width, height = 500, 300
    screen_w = splash.winfo_screenwidth()
    screen_h = splash.winfo_screenheight()
    x = (screen_w - width) // 2
    y = (screen_h - height) // 2
    splash.geometry(f"{width}x{height}+{x}+{y}")

    # Logo loading (optional fallback to text)
    try:
        logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
        logo = Image.open(logo_path)
        logo = logo.resize((200, 200))
        logo_img = ImageTk.PhotoImage(logo)
        tk.Label(splash, image=logo_img, bg="#111111").pack(pady=10)
        splash.logo_img = logo_img
    except Exception as e:
        print(f"[!] Logo error: {e}")
        tk.Label(splash, text="AnujScan", font=("Helvetica", 24, "bold"),
                 fg="#00ffd5", bg="#111111").pack(pady=50)

    tk.Label(splash, text="Launching AnujScan Toolkit...",
             font=("Helvetica", 12), fg="#00ffd5", bg="#111111").pack(pady=10)

    # Launch GUI after 2.5 seconds
    splash.after(2500, lambda: (splash.destroy(), launch_gui()))

    splash.mainloop()

if __name__ == "__main__":
    show_splash()
