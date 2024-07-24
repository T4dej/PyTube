from pytube import YouTube  # type: ignore
import os
import re

# Get the directory where the script is running
script_dir = os.path.dirname(os.path.abspath(__file__))

def sanitize_filename(filename: str) -> str:
    # Remove or replace invalid characters for filenames
    return re.sub(r'[\\/*?:"<>|]', "_", filename)

def downloadMp3(url: str):
    try:
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
        print(f"The music '{full_title}' is downloaded in MP3")
    except Exception as e:
        print(f"Unable to fetch video information. Error: {e}")

def downloadMp4(url: str):
    yt = YouTube(url)  
    try:
        # Ensure the /mp4 directory exists in the script directory
        mp4_dir = os.path.join(script_dir, 'mp4')
        if not os.path.exists(mp4_dir):
            os.makedirs(mp4_dir)

        # Get the title and author
        video_title = yt.title
        video_author = yt.author
        full_title = sanitize_filename(f"{video_author} - {video_title}")
        
        yt.streams.filter(progressive=True, file_extension="mp4").first().download(output_path=mp4_dir, filename=full_title)
        print(f"The video '{full_title}' is downloaded in MP4")
    except Exception as e:
        print(f"Unable to fetch video information. Error: {e}")

def get_valid_choice():
    while True:
        try:
            choise = input("Download mp3 (press 1), or mp4 (press 2), for exit press 3: ").strip()
            if choise == '':
                print("Input cannot be empty. Please enter a valid option.")
                continue
            choise = int(choise)
            if choise in [1, 2, 3]:
                return choise
            else:
                print("Not a valid option! Please enter 1, 2, or 3.")
        except ValueError:
            print("Please enter a valid number (1, 2, or 3).")

while True:
    choise = get_valid_choice()

    if choise == 1:
        url = input("Enter url: ").strip()
        if url:
            downloadMp3(url)
        else:
            print("URL cannot be empty. Please enter a valid URL.")
    elif choise == 2:
        url = input("Enter url: ").strip()
        if url:
            downloadMp4(url)
        else:
            print("URL cannot be empty. Please enter a valid URL.")
    elif choise == 3:
        print("Exiting...")
        break