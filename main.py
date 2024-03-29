# IMPORTS
from PIL import Image, ImageDraw, ImageFont
import requests
import textwrap
import googleapiclient.discovery
import dotenv
import os

import utils_convertor



# CONSTANTS

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

# the border radius of the thumbnail is calculated with the width of the image divided by this number, increase it to make the thumbnail more rounded
BORDER_RADIUS_THUMBNAIL_ANGLE = 12

# the border radius of the rectangle is in pixels
BORDER_RADIUS_RECTANGLE = 20

# opacity of the background rectangle (0 = transparent, 255 = opaque)
BACKGROUND_OPACITY = 150

# the name of the thumbnail image is useless because it will be deleted at the end
THUMBNAIL_YT_NAME = "youtube_thumbnail.png"

# u can change the font if u want but don't remove it
PRIMARY_FONT = CURRENT_PATH + "/Roboto-Black.ttf"
ADDITIONAL_FONT = CURRENT_PATH + "/Roboto-Light.ttf"



video_id = utils_convertor.get_youtube_video_id(input("URL de la vidéo YouTube: "))


# GET VIDEO INFORMATIONS
utils_convertor.checklist(0)

# Get API key from .env file
dotenv.load_dotenv()
api_key = os.getenv("API_KEY")

# Create an instance of the YouTube Data API v3 service
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

# Retrieve video information by its ID
response = youtube.videos().list(part="snippet,statistics", id=video_id).execute()

# Retrieve the video information from the response
video_title = response['items'][0]['snippet']['title']
view_count = response['items'][0]['statistics']['viewCount']
channel_title = response['items'][0]['snippet']['channelTitle']

# Retrieve youtube thumbnail and try to get the highest resolution
resolution_order = ['maxres', 'standard', 'high', 'medium', 'default']
for resolution in resolution_order:
    if resolution in response['items'][0]['snippet']['thumbnails']:
        thumbnail_url = response['items'][0]['snippet']['thumbnails'][resolution]['url']
        break
        
response_thumbnail = requests.get(thumbnail_url)

# Save image locally
with open(f"{CURRENT_PATH}/{THUMBNAIL_YT_NAME}", "wb") as img_file:
    img_file.write(response_thumbnail.content)


print("Miniature téléchargée avec succès.")



# ROUND UP THE THUMBNAIL
utils_convertor.checklist(1)

# I've rounded in pixels, not percentages, so it only works at maximum resolution, otherwise it might create a texture bug.
im = Image.open(f"{CURRENT_PATH}/{THUMBNAIL_YT_NAME}")

# Removing black lines from top to bottom
for y in range(im.height):
    pixel_color = im.getpixel((0, y))
    
    if all(color == 0 for color in pixel_color[:3]):
        im = im.crop((0, y, im.width, im.height))
    else:
        break

# Removing black lines from bottom to top
for y in reversed(range(im.height)):
    pixel_color = im.getpixel((0, y))
    
    if all(color == 0 for color in pixel_color[:3]):
        im = im.crop((0, 0, im.width, y))
    else:
        break


border_radius_thumbnail = im.size[0] // BORDER_RADIUS_THUMBNAIL_ANGLE


# Create a circular mask for rounding
circle_mask = Image.new('L', (border_radius_thumbnail * 2, border_radius_thumbnail * 2), 0)
draw = ImageDraw.Draw(circle_mask)
draw.ellipse((0, 0, border_radius_thumbnail * 2 - 1, border_radius_thumbnail * 2 - 1), fill=255)

# Create an alpha mask with the rounded circle
alpha = Image.new('L', im.size, 255)
w, h = im.size
alpha.paste(circle_mask.crop((0, 0, border_radius_thumbnail, border_radius_thumbnail)), (0, 0))
alpha.paste(circle_mask.crop((0, border_radius_thumbnail, border_radius_thumbnail, border_radius_thumbnail * 2)), (0, h - border_radius_thumbnail))
alpha.paste(circle_mask.crop((border_radius_thumbnail, 0, border_radius_thumbnail * 2, border_radius_thumbnail)), (w - border_radius_thumbnail, 0))
alpha.paste(circle_mask.crop((border_radius_thumbnail, border_radius_thumbnail, border_radius_thumbnail * 2, border_radius_thumbnail * 2)), (w - border_radius_thumbnail, h - border_radius_thumbnail))

# Save image locally
im.putalpha(alpha)
im.save(f"{CURRENT_PATH}/{THUMBNAIL_YT_NAME}")

    

# BACKGROUND
utils_convertor.checklist(2)

# Create a new 1920x1080 image with a transparent background
width, height = 1920, 1080
image = Image.new("RGBA", (width, height), (0, 0, 0, 0))



# ROUNDED RECTANGLE
utils_convertor.checklist(3)

# Create an object to draw on the image
draw = ImageDraw.Draw(image)

# Coordinates and dimensions of the rounded rectangle
rect_x, rect_y = 30, height - 200
rect_width, rect_height = 700, 170

# Draw the rectangle
draw.rectangle([(rect_x + BORDER_RADIUS_RECTANGLE, rect_y), (rect_x + rect_width - BORDER_RADIUS_RECTANGLE, rect_y + rect_height)], fill=(60, 60, 60, BACKGROUND_OPACITY))
draw.rectangle([(rect_x, rect_y + BORDER_RADIUS_RECTANGLE), (rect_x + rect_width, rect_y + rect_height - BORDER_RADIUS_RECTANGLE)], fill=(60, 60, 60, BACKGROUND_OPACITY))

# Add rounded corners
draw.pieslice([(rect_x, rect_y), (rect_x + BORDER_RADIUS_RECTANGLE * 2, rect_y + BORDER_RADIUS_RECTANGLE * 2)], 180, 270, fill=(60, 60, 60, BACKGROUND_OPACITY))
draw.pieslice([(rect_x, rect_y + rect_height - BORDER_RADIUS_RECTANGLE * 2), (rect_x + BORDER_RADIUS_RECTANGLE * 2, rect_y + rect_height)], 90, 180, fill=(60, 60, 60, BACKGROUND_OPACITY))
draw.pieslice([(rect_x + rect_width - BORDER_RADIUS_RECTANGLE * 2, rect_y), (rect_x + rect_width, rect_y + BORDER_RADIUS_RECTANGLE * 2)], 270, 360, fill=(60, 60, 60, BACKGROUND_OPACITY))
draw.pieslice([(rect_x + rect_width - BORDER_RADIUS_RECTANGLE * 2, rect_y + rect_height - BORDER_RADIUS_RECTANGLE * 2), (rect_x + rect_width, rect_y + rect_height)], 0, 90, fill=(60, 60, 60, BACKGROUND_OPACITY))



# TITLE OF THE VIDEO
utils_convertor.checklist(4)

# Show the title of the video
font = ImageFont.truetype(PRIMARY_FONT, 25)

# Text coordinates
text_x = rect_x + 280
text_y = rect_y + 20

# Split text into several lines
wrapped_text = textwrap.wrap(video_title, width=33)

# Draw each line on the rectangle with a maximum of 2 lines
max_lines = 2
for i, line in enumerate(wrapped_text):
    if i < max_lines - 1:
        # Draw text
        draw.text((text_x, text_y), line, fill=(255, 255, 255), font=font)
        # Go to the next line with a space
        text_y += font.getsize(line)[1] + 5  
    else:
        # Remaining space before suspension points
        remaining_space = 35 - len(line)
        if remaining_space <= 3:
            # Replace last caracters by suspension points if there is not enough space
            line = line[:35 - 3] + "..."
        draw.text((text_x, text_y), line, fill=(255, 255, 255), font=font)
        break 



# CHANNEL NAME AND VIEWS COUNT
utils_convertor.checklist(5)

# Add suspension points if the channel name is too long
if len(channel_title) > 19:
    channel_title = channel_title[0:19 - 3] + "..."

# Add the channel name and the number of views in the same variable
additional_text = channel_title + " • " + utils_convertor.format_large_number(view_count) + " vues"
additional_font = ImageFont.truetype(ADDITIONAL_FONT, 25)

# Coordinates of additional text
additional_text_x = text_x
additional_text_y = rect_y + rect_height - 50  # Décalage vers le bas pour le texte supplémentaire

draw.text((additional_text_x, additional_text_y), additional_text, fill=(255, 255, 255), font=additional_font)



# SHOW THUMBNAIL
utils_convertor.checklist(6)

# Open and resize thumbnail
thumbnail_image = Image.open(f"{CURRENT_PATH}/{THUMBNAIL_YT_NAME}").convert("RGBA")
new_width  = 16 * 15
new_height = int(round(new_width * thumbnail_image.size[1] / thumbnail_image.size[0], 0))
thumbnail_image = thumbnail_image.resize((new_width, new_height))

# Coordinates of the thumbnail (centered vertically)
thumbnail_x = rect_x + 15
thumbnail_y = rect_y + (rect_height - thumbnail_image.height) // 2

image.alpha_composite(thumbnail_image, (thumbnail_x, thumbnail_y))



# DELETE THUMBNAIL
utils_convertor.checklist(7)

if os.path.exists(f"{CURRENT_PATH}/{THUMBNAIL_YT_NAME}"):
    os.remove(f"{CURRENT_PATH}/{THUMBNAIL_YT_NAME}")
else:
    print(f"The file {THUMBNAIL_YT_NAME} doesn't exist")


# SAVE FINAL IMAGE
utils_convertor.checklist(8)

image.save(f"{CURRENT_PATH}/{utils_convertor.format_filename(video_title)}.png", format="PNG")

utils_convertor.checklist(9)
