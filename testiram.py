import tkinter as tk
from tkinter import messagebox
from pytube import YouTube  # type: ignore
import os
import re
import threading

# Get the directory where the script is running
script_dir = os.path.dirname(os.path.abspath(__file__))

def sanitize_filename(filename: str) -> str:
    # Remove or replace invalid characters for filenames
    return re.sub(r'[\\/*?:"<>|]', "_", filename)

def downloadMp3(url: str, button):
    try:
        button.config(text="Downloading...", state=tk.DISABLED)
        mp4_button.config(state=tk.DISABLED)
        exit_button.config(state=tk.DISABLED)
        video = YouTube(url)
        stream = video.streams.filter(only_audio=True).first()
        
        # Ensure the /mp3 directory exists in the script directory
        mp3_dir = os.path.join(script_dir, 'mp3')
        if not os.path.exists(mp3_dir):
            os.makedirs(mp3_dir)
        
        # Get the title and author
        video_title = video.title
        video_author = video.author
        full_title = sanitize_filename(f"{video_author} - {video_title}")
        
        stream.download(output_path=mp3_dir, filename=f"{full_title}.mp3")
        messagebox.showinfo("Success", f"The music '{full_title}' is downloaded in MP3")
    except Exception as e:
        messagebox.showerror("Error", f"Unable to fetch video information. Error: {e}")
    finally:
        button.config(text="Download MP3", state=tk.NORMAL)
        mp4_button.config(state=tk.NORMAL)
        exit_button.config(state=tk.NORMAL)

def downloadMp4(url: str, button):
    try:
        button.config(text="Downloading...", state=tk.DISABLED)
        mp3_button.config(state=tk.DISABLED)
        exit_button.config(state=tk.DISABLED)
        yt = YouTube(url)  
        # Ensure the /mp4 directory exists in the script directory
        mp4_dir = os.path.join(script_dir, 'mp4')
        if not os.path.exists(mp4_dir):
            os.makedirs(mp4_dir)

        # Get the title and author
        video_title = yt.title
        video_author = yt.author
        full_title = sanitize_filename(f"{video_author} - {video_title}")
        
        yt.streams.filter(progressive=True, file_extension="mp4").first().download(output_path=mp4_dir, filename=full_title)
        messagebox.showinfo("Success", f"The video '{full_title}' is downloaded in MP4")
    except Exception as e:
        messagebox.showerror("Error", f"Unable to fetch video information. Error: {e}")
    finally:
        button.config(text="Download MP4", state=tk.NORMAL)
        mp3_button.config(state=tk.NORMAL)
        exit_button.config(state=tk.NORMAL)

def on_download_mp3():
    url = url_entry.get().strip()
    if url:
        threading.Thread(target=downloadMp3, args=(url, mp3_button)).start()
        url_entry.delete(0, tk.END)  # Clear the URL entry
    else:
        messagebox.showwarning("Input Error", "URL cannot be empty. Please enter a valid URL.")

def on_download_mp4():
    url = url_entry.get().strip()
    if url:
        threading.Thread(target=downloadMp4, args=(url, mp4_button)).start()
        url_entry.delete(0, tk.END)  # Clear the URL entry
    else:
        messagebox.showwarning("Input Error", "URL cannot be empty. Please enter a valid URL.")

def on_exit():
    root.destroy()

# Setting up the Tkinter GUI
root = tk.Tk()
root.title("YouTube Downloader")

# URL input field
tk.Label(root, text="Enter YouTube URL:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5, padx=20)

# Buttons for MP3 and MP4 download
mp3_button = tk.Button(root, text="Download MP3", command=on_download_mp3)
mp3_button.pack(pady=5, padx=20)

mp4_button = tk.Button(root, text="Download MP4", command=on_download_mp4)
mp4_button.pack(pady=5, padx=20)

# Exit button
exit_button = tk.Button(root, text="Exit", command=on_exit)
exit_button.pack(pady=5, padx=20)

# Start the Tkinter main loop
root.mainloop()