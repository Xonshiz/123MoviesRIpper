# [new-movies123.co Downloader](https://new-movies123.co/)
Script to bypass resolution and IP Limit on new-movies123.co

This script will download both, an mp4 1080p (or the next highest available stream) and subtitles (.srt).

Just download the proper binary and execute it. It'll ask for the URL, paste the URL and wait till the script downloads the series.

**NOTE** : Must have youtube-dl installed and available in path.

# Things To Know
- It'll work for TV Series.
- I have not yet tested this with Movies and I'm 90% sure that it'll break.
- Required "Youtube-dl" to download the video streams.
- It's best to provide URL of the 1st episode, because this script doesn't have proper validations and will throw errors if a file already exists.
- If you can't find binary for your operating system, that means TravisCI had issues making a binary and you would need to install python and download the code from this repository and then run it yourself.

# Running Python Code
- Download the code from this repository.
- Open terminal and go into 123MoviesRipper directory and run this command: `pip install -r requirements.txt`.
- Then you can move into src directory in your terminal.
- When you're into src directory, run this command: `python __main__.py`


P.S: This is a script I hacked around last night, because amazon prime decided not to make season 3 of "D" available in most regions and this website was the only way to grab the episodes.

Welp, use with caution. And as usual, no harm intended via this script.

Please do use the script carefully, don't hog the website bandwidth.
