import requests
import urllib.request
import re 
import youtube_dl
import os
import sys
from termcolor import colored

def playList(url):
	result = []
	url = url.split("?si")[0] + "?utm_source=generator"
	url = url.replace("/playlist/", "/embed/playlist/")
	page = requests.get(url)
	words = ["external_urls", "id%22%3A%22", "images", "width%22%3A", "owner", "type", "uri", "tracks", "track", "items", "added_by", "dominantColor", " ", "artist", "release_date", "total_tracks", "is_local", "popularity"]
	soup = page.text.split("<script id=\"resource\" type=\"application/json\">")[1].replace("%2C%22name%22%3A%22","specialCharacter").replace("%22%2C%22","specialCharacter").split("specialCharacter")

	names = []
	for i in soup:
		controller = True
		for l in words:
			if i.startswith(l):
				controller = False
		if controller:
			names.append(i)
	names.pop(0)
	names.pop(0)

	songnum = int(len(names)/4)

	fullnames = []
	for i in range(songnum):
		artist = names[0]
		name = names[3]
		fullnames.append(artist+"-"+name)
		names.pop(0)
		names.pop(0)
		names.pop(0)
		names.pop(0)

	return fullnames

def playListControl(names):
	while True:
		print(colored("There Are The Names Of Songs We Find From The Spotify Playlist Link You Gave:","green"))
		for i,l in enumerate(names):
			l = l.replace("%20"," ")
			print(f"[{i}] {l}" )
		process = input("Press A to Add Music, D to Delete Music, C to continue:\t").upper()
		if process == "C":
			break 
		elif process == "A":
			music = input("Write the name of the artist and the music:\t\t")
			music = music.replace(" ", "%20")
			names.append(music)
		elif process == "D":
			num = int(input("What is the number of the name you want to delete:\t"))
			names.pop(num)
		else:
			print("Unvalid process")
		os.system("cls")
	os.system("cls")	
	return names

def searchLink(track_names):
	urls = []
	for i in track_names:
		urls.append(f"https://www.youtube.com/results?search_query={i}")
	return urls

def videoIds(urls):
	result = []
	for i in urls:
		html = urllib.request.urlopen(i)
		video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
		result.append(f"https://www.youtube.com/watch?v={video_ids[0]}")
	return result

def videoIdsControl(videoLinks):
	ydl_opts = {
		'quiet': True
	}
	youtube_dl_manager = youtube_dl.YoutubeDL(ydl_opts)
	while True:
		print(colored("There Are The Youtube Links Of Songs We Find From The Spotify Playlist Link You Gave:","green"))
		for i,l in enumerate(videoLinks):
			video_info = youtube_dl_manager.extract_info(url = l,download=False)
			title = video_info["title"]
			print(f"[{i}] {title} ({l})" )
		process = input("Press A to Add Music Link, D to Delete Music Link, C to continue:\t").upper()
		if process == "C":
			break 
		elif process == "A":
			music = input("Paste the youtube link of the music:\t\t")
			music = music.replace(" ", "%20")
			videoLinks.append(music)
		elif process == "D":
			num = int(input("What is the number of the link you want to delete:\t"))
			videoLinks.pop(num)
		else:
			print("Unvalid process")

		os.system("cls")
	os.system("cls")
	return videoLinks

def download(urlList):
	for video_url in urlList:
		video_info = youtube_dl.YoutubeDL().extract_info(
			url = video_url,download=False
		)
		filename = f"{video_info['title']}.mp3"
		filename = filename.replace("/", "-")
		options={
			'format':'bestaudio/best',
			'keepvideo':False,
			'outtmpl':filename,
			'quiet':True,
		}

		with youtube_dl.YoutubeDL(options) as ydl:
		    ydl.download([video_info['webpage_url']])

		print(colored(f"Download complete... {filename}","green"))
