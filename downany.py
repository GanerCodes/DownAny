import os
from subprocess import Popen
from hashlib import sha256

qsha = lambda data: sha256(data.encode()).hexdigest()

collapseList = lambda l, n = None: (collapseList(l, j := []) and j) if n is None else ([collapseList(i, n) for i in l] if isinstance(l, list) else n.append(l))

def downloadYoutube(link, noPlaylist = False, audioOnly = False, folder = "", cookies = "cookies.txt"):
    return (folder, Popen(collapseList([
        "yt-dlp", ['-x', "--audio-format", "mp3"] if audioOnly else ["--merge-output-format", "mp4"], "--no-progress", "--embed-thumbnail",
        "--no-post-overwrites", "-ciw", ["--no-playlist"] if noPlaylist else [], "--cookies", cookies, "--restrict-filenames",
        "-o", f"{folder}/%(playlist_index)s_%(title)s_%(id)s.%(ext)s", link
    ])))

def downloadGallery(link, folder = "", cookies = "cookies.txt"):
    return (folder, Popen(collapseList([
        "gallery-dl", "--config", "gallery_dl.json", "--cookies", cookies, "-o", f"base-directory={folder}", link
    ])))

def downloadWget(link, folder = "", cookies =  "cookies.txt"):
    return (folder, Popen(collapseList([
        "wget", "--load-cookies", cookies, "-c", "-nd", "-nv", "-P", f"{folder}", link
    ])))

def download(link, args = "", baseDir = "download", cookies = "cookies.txt"):
    args = list(filter(None, args.lower().split(' ')))
    baseFold = f"{baseDir}/{(hsh := qsha(link)[:24])}"
    
    print(f'''Downloading "{link}" with args "{', '.join(args)}" to location "{baseFold}"''')
    procs = []
    if len(args) == 0:
        print("No downloader options provided, trying video, gallery, and wget")
        args = "video gallery wget"
    if "video" in args:
        print("Downloading as: video")
        procs.append(("video", downloadYoutube(link, audioOnly = 0, noPlaylist = ("noplaylist" in args), folder = f"{baseFold}/video", cookies = cookies)))
    if "audio" in args:
        print("Downloading as: audio")
        procs.append(("audio", downloadYoutube(link, audioOnly = 1, noPlaylist = ("noplaylist" in args), folder = f"{baseFold}/audio", cookies = cookies)))
    if "gallery" in args or "image" in args:
        print("Downloading as: gallery")
        procs.append(("gallery", downloadGallery(link, folder = f"{baseFold}/gallery", cookies = cookies)))
    if "wget" in args or "file" in args:
        print("Downloading as: wget")
        procs.append(("wget", downloadWget(link, folder = f"{baseFold}/wget", cookies = cookies)))
    
    final = []
    for proc in procs:
        t, p = proc
        p[1].wait()
        expectedDir = f"{baseFold}{p[0]}"
        if os.path.exists(expectedDir) and len(dr := os.listdir(expectedDir)):
            final.append((t, p[1].returncode, f"{expectedDir}/{dr[0]}" if len(dr) == 1 else expectedDir))
    
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