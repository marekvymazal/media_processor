# Media Processor
Convert raw / original media to web ready media
* Watermark
* Resize images / video
* Convert video to gifs
* Convert image sequence to mp4
* Export galleries with thumbnails
* Read media.xml and processes all files (website)
* wav to mp3
* png to jpg
* svg files to wallpapers
* svg files to icons

# Setup
### ffmpeg installation
ffmpeg needs to be in bin folder
/usr/local/bin
open .

# TODO
- [X] Only process files that don't exist in output folder
- [X] Delete files that are not listed in data in target folders
- [ ] Support for specifying svg icon sizes
- [ ] Wallpaper / Icon tag support in media.xml files ( specify svg to convert to a wallpaper or icon at destination )
- [ ] Watermark enable/disable override per category or item
- [ ] Target width/height in xml, for thumbnails too
- [ ] svg to jpg or png
- [ ] image sequence to video or gif
- [ ] init command that generates template data xml file
