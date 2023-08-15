# yt-thumbnail-sources

### FR
Ce projet à pour but d'extraire la miniature d'une vidéo Youtube ainsi que l'auteur la vidéo afin de pouvoir citer la dite vidéo en l'incluant dans votre propore vidéo. (c'est mal expliqué je sais)

### EN
The aim of this project is to extract the thumbnail from a Youtube video and its author to cite the source by including it in your own video.

## How to Get a YouTube API Key
- Log in to <a href="https://console.cloud.google.com/">Google Developers Console</a>.
- Create a new project.
- On the new project dashboard, click Explore & Enable APIs.
- In the library, navigate to YouTube Data API v3 under YouTube APIs.
- Enable the API.
- Create a credential.
- A screen will appear with the API key.

## Exemple
<a href="https://github.com/Ashokaas/yt-thumbnail-sources/assets/99681959/afda7256-79e5-479b-993a-57f2d628aa00" download>output.png</a>
<br>
<img src="https://github.com/Ashokaas/yt-thumbnail-sources/assets/99681959/01555242-1fe9-499e-823d-578a3be231c3" width="50%">

## Editable parameters

```
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
```

<br><br><br>

<i>sorry for my bed england</i>

