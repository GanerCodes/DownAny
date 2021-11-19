Pretty simple "just works" type downloader, really easy to link to a Discord bot or something

Install:
`pip install -r requirements.txt`

Use:
`python downany.py <link> <args>`

Args are:  
    Video: for yt-dlp  
    Audio: also yt-dlp but extracts audio  
    Gallery OR image: for gallery-dl  
    File OR wget: for wget  
    NoPlaylist: disable entire playlist downloading for video and audio args
