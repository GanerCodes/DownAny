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
    baseFold = f"{baseDir}/{(hsh := qsha(link)[:24])}"
    
    print(f'''Downloading "{link}" with args "{', '.join(args)}" to location "{baseFold}"''')
    procs = []
    if len(args) == 0:
        print("No downloader options provided, trying video, gallery, and wget")
        args = "video gallery wget"
    if "video" in args:
        print("Downloading as: video")
        procs.append(("video", downloadYoutube(link, audioOnly = 0, noPlaylist = ("noplaylist" in args), folder = f"{baseFold}/video")))
    if "audio" in args:
        print("Downloading as: audio")
        procs.append(("audio", downloadYoutube(link, audioOnly = 1, noPlaylist = ("noplaylist" in args), folder = f"{baseFold}/audio")))
    if "gallery" in args or "image" in args:
        print("Downloading as: gallery")
        procs.append(("gallery", downloadGallery(link, folder = f"{baseFold}/gallery")))
    if "wget" in args or "file" in args:
        print("Downloading as: wget")
        procs.append(("wget", downloadWget(link, folder = f"{baseFold}/wget")))
    
    final = []
    for proc in procs:
        t, p = proc
        p[1].wait()
        if os.path.exists(p[0]) and len(dr := os.listdir(p[0])):
            final.append((t, p[1].returncode, f"{p[0]}/{dr[0]}" if len(dr) == 1 else p[0]))
    
    return final

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