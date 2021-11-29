# M3U8 Downloader
Provided the link to an M3U8 playlist, this script rapidly downloads all the contained videos, 
then fuses them into a single MP4 using FFmpeg. Note that if you do not have FFmpeg, comment out the lines 
that call os.system(), then play the downloaded playlist using the `index.m3u8` file.

## Usage
Call `download.py link output_filename`, replacing `link` with the link to your M3U8 playlist, and 
`output_filename` with the filename you would like for the converted MP4. Note that if you remove 
the `os.system()` call, then the output_filename will be ignored.