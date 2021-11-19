import os
from subprocess import Popen
from hashlib import sha256

qsha = lambda data: sha256(data.encode()).hexdigest()

collapseList = lambda l, n = None: (collapseList(l, j := []) and j) if n is None else ([collapseList(i, n) for i in l] if isinstance(l, list) else n.append(l))

def downloadYoutube(link, noPlaylist = False, audioOnly = False, folder = ""):
    return (folder, Popen(collapseList([
        "yt-dlp", ['-x', "--audio-format", "mp3"] if audioOnly else ["--merge-output-format", "mp4"], "--no-progress", "--embed-thumbnail",
        "--no-post-overwrites", "-ciw", ["--no-playlist"] if noPlaylist else [], "--cookies", "cookies.txt", "--restrict-filenames",
        "-o", f"{folder}/%(playlist_index)s_%(title)s_%(id)s.%(ext)s", link
    ])))

def downloadGallery(link, folder = ""):
    return (folder, Popen(collapseList([
        "gallery-dl", "--config", "gallery_dl.json", "-o", f"base-directory={folder}", link
    ])))

def downloadWget(link, folder = ""):
    return (folder, Popen(collapseList([
        "wget", "--load-cookies", "cookies.txt", "-c", "-nd", "-nv", "-P", f"{folder}", link
    ])))

def download(link, args = "", baseDir = "download"):
    args = list(filter(None, args.lower().split(' ')))
    baseFold = f"{baseDir}/{hsh := qsha(link)[:24]}"
    
    print(f'''Downloading "{link}" with args "{', '.join(args)}" to location "{}"''')
    procs = []
    if len(args) == 0:
        print("No downloader options provided, trying video, gallery, and wget")
        args = "video gallery wget"
    if "video" in args:
        print("Downloading as: video")
        procs.append(downloadYoutube(link, audioOnly = 0, noPlaylist = ("noplaylist" in args), folder = f"{baseFold}/video"))
    if "audio" in args:
        print("Downloading as: audio")
        procs.append(downloadYoutube(link, audioOnly = 1, noPlaylist = ("noplaylist" in args), folder = f"{baseFold}/audio"))
    if "gallery" in args or "image" in args:
        print("Downloading as: gallery")
        procs.append(downloadGallery(link, folder = f"{baseFold}/gallery"))
    if "file" in args or "wget" in args:
        print("Downloading as: file")
        procs.append(downloadWget(link, folder = f"{baseFold}/wget"))
    
    return [(i[1].returncode, i[0]) for i in procs if i[1].wait() or True]

if __name__ == "__main__":
    from sys import argv
    r = None
    if len(argv) < 2:
        r = download("https://www.youtube.com/watch?v=Rmea5ET_n9g")
    elif len(argv) == 2:
        r = download(argv[1])
    else:
        r = download(argv[1], ' '.join(argv[2:]))
    print(f"Result: {r}")