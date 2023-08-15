#IMPORTS
import re
import os
import sys


def get_youtube_video_id(url:str):
    """Returns the ID of a YouTube video from its URL.
    Raises a ValueError if the URL is invalid.

    Args:
        url (str): URL of the video

    Raises:
        ValueError: Invalid YouTube URL provided

    Returns:
        str: video id
    """
    if len(url) == 11:
        return url

    regex_patterns = [
        r"v=([a-zA-Z0-9_-]+)",                # http://www.youtube.com/watch?v=VIDEO_ID
        r"user/[a-zA-Z0-9_-]+#p/a/u/\d+/\w+", # http://www.youtube.com/user/USER_ID#p/a/u/1/VIDEO_ID
        r"/v/([a-zA-Z0-9_-]+)\?",             # http://www.youtube.com/v/VIDEO_ID?fs=1&amp;hl=en_US&amp;rel=0
        r"v=([a-zA-Z0-9_-]+)#t=\w+",          # http://www.youtube.com/watch?v=VIDEO_ID#t=0m10s
        r"/embed/([a-zA-Z0-9_-]+)\?",         # http://www.youtube.com/embed/VIDEO_ID?rel=0
        r"youtu\.be/([a-zA-Z0-9_-]+)"         # http://youtu.be/VIDEO_ID
    ]

    for pattern in regex_patterns:
        match = re.search(pattern, url)
        if match:
            video_id = match.group(1)
            return video_id

    raise ValueError("Invalid YouTube URL provided.")


def format_large_number(number:str):
    """Formats a large number to a more readable format.

    Args:
        number (str): the number to format

    Returns:
        int: the formatted number
    """
    number = int(number)
    units = ["", "K", "M", "B", "T"]  # Unités pour les milliers, millions, milliards, etc.
    unit_index = 0

    while number >= 1000 and unit_index < len(units) - 1:
        number /= 1000
        unit_index += 1

    formatted_number = f"{number:.1f}{units[unit_index]}"
    return formatted_number


def format_filename(text:str):
    """Formats a string to be used as a filename.

    Args:
        text (str): video name

    Returns:
        str: video filename
    """
    allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ")
    cleaned_text = "".join(c if c in allowed_chars else "_" for c in text)
    cleaned_text = cleaned_text.replace(' ', '_')
    cleaned_text = cleaned_text.lower()
    return cleaned_text



def clear_console():
    """Clears the console screen."""
    # Windows
    if sys.platform.startswith("win"):
        os.system("cls")
    # Unix/Linux/MacOS
    else:
        os.system("clear")


def checklist(current_step:int):
    """Show the current step of the process.

    Args:
        current_step (int): current step of the process

    Returns:
        None: None
    """
    clear_console()
    emojis = ["✔️", "❌", "⏳"]
    all_steps = ["Retrieving video informations/Downloading the thumbnail...",
             "Rounding up the thumbnail...",
             "Creating the background...",
             "Adding the title...",
             "Adding the channel name and the view counter...",
             "Adding the thumbnail...",
             "Deleting the thumbnail...",
             "Saving the final image..."]

    for step in range(len(all_steps)):
        if step < current_step:
            print(f"{emojis[0]}  {all_steps[step]}")
        elif step == current_step:
            print(f"{emojis[2]}  {all_steps[step]}")
        else:
            print(f"{emojis[1]}  {all_steps[step]}")

