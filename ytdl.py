#!/usr/bin/python3

from pytube import YouTube
import os
import datetime
import sys

def combine_audio(vidname, audname, outname, fps = 30): 
    import moviepy.editor as mpe
    my_clip = mpe.VideoFileClip(vidname)
    audio_background = mpe.AudioFileClip(audname)
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(outname,fps = fps)

os.chdir("/mnt/chromeos/MyFiles/Downloads/YT")

print("Current directory: " + os.getcwd())
os.system("ls -d */")
ogdir = input("Change directory? Choose one (or make a new one): ").replace("\n", "")
dir = ogdir
dir.replace(" ", "_")
while not ogdir == "":
    if ogdir == "cd ..":
        os.chdir(ogdir.replace("cd ", ""))
    elif ogdir.startswith("cd"):
        os.chdir(ogdir.replace("cd ", ""))
    elif os.path.isdir("/mnt/chromeos/MyFiles/Downloads/YT/" + dir):
        os.chdir("/mnt/chromeos/MyFiles/Downloads/YT/" + dir)
        break
    else:
        os.mkdir("/mnt/chromeos/MyFiles/Downloads/YT/" + dir)
        os.chdir("/mnt/chromeos/MyFiles/Downloads/YT/" + dir)
        break
    print("Current directory: " + os.getcwd() + '\n')
    os.system("ls -d */")
    ogdir = input("Change directory? Choose one (or make a new one): ").replace("\n", "")

link = input("Link: ")

yt = YouTube(link)

print("Title: " + yt.title)
print("Views: ", yt.views)
print("Length: ", str(datetime.timedelta(seconds = yt.length)))

if input("Confirm that this is correct? [Y/N] ").lower() == "y":
    print(str(yt.streams.filter(file_extension = "mp4").order_by("resolution")).replace(",", "\n\n"))
    # print(str(yt.streams.all).replace(", ", "\n\n")) 
    print("File size: at most ", yt.streams.get_highest_resolution().filesize_approx / 1000000, "MB")
    stream = input("Which stream would you like to download? ")
    dl = yt.streams.get_by_itag(stream)
    
    print("Downloading...")
    dl.download(None, yt.title.replace(":", "_").replace(" ", "_").replace("*", "_").replace("/", "_").replace("|", "_") + ".mp4")
    print("Done download.")
    
    if dl.is_progressive:
        sys.exit
    
    print(str(yt.streams.filter(only_audio = True, file_extension = "mp4")).replace(", ", "\n\n"))
    stream = input("Select an audio to go with it: ")
    dl = yt.streams.get_by_itag(stream)
    print("Downloading...")
    dl.download(None, yt.title.replace(":", "_").replace(" ", "_").replace("*", "_").replace("/", "_").replace("|", "_") + ".mp3") 
    print("Done download.")
    
    print("Merging")
    combine_audio(yt.title.replace(":", "_").replace(" ", "_").replace("*", "_").replace("/", "_").replace("|", "_") + ".mp4", yt.title.replace(":", "_").replace(" ", "_").replace("*", "_").replace("/", "_").replace("|", "_") + ".mp3", "temp.mp4")
    os.remove(yt.title.replace(":", "_").replace(" ", "_").replace("*", "_").replace("/", "_").replace("|", "_") + ".mp4")
    os.rename("temp.mp4", yt.title.replace(":", "_").replace(" ", "_").replace("*", "_").replace("/", "_").replace("|", "_") + ".mp4")
    
    if input("Delete audio? [Y/N] ").lower() == y:
        os.remove(yt.title.replace(":", "_").replace(" ", "_").replace("*", "_").replace("/", "_").replace("|", "_") + ".mp3")
