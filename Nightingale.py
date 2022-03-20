from functions import *

def main():
	url = str(input("Spotify playlist url:"))

	track_names = playList(url)
	track_names = playListControl(track_names)
	urls = searchLink(track_names)
	videoLinks = videoIds(urls)
	videoLinks = videoIdsControl(videoLinks)
	download(videoLinks)

if __name__ == "__main__":
	main()