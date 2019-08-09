import sys

import os
import shutil
import xml.etree.ElementTree as ET

import getopt
import shutil, errno
from pathlib import Path
import html5lib
import base64

from . import settings
from . import data
from . import audio
from . import svg


def main():

    argv = sys.argv[1:]

    help_str = """
    Copyright 2019 Marek Vymazal

    -h,--help              Show help
    --data <data.xml>      Processes data file
    --delete               Delete files in target folder that are not listed in data file
    --new                  Only create files that don't already exist

    --init                 //todo Create template media.xml file

    When calling in directory the media processor will automatically convert:

        Audio
        .wav -> .mp3

        Video
        .mov -> .mp4 //todo
        .avi -> .mp4 //todo

        Image Sequence
        .#.png -> .mp4 //todo
        .#.jpg -> .mp4 //todo

    --crawl //todo Crawl up directories from current working directory and process those files

    -i ext -o ext //todo Convert only files of input extension to files of output extension
    ex: -i jpg -o png
    ex: -i gif -o mp4

    svg:
        --svg-wallpaper    Export wallpapers
        --svg-icon         Export icons
    """

    data_file = None

    try:
        opts, args = getopt.getopt(argv,"h",["help","data=","delete","new","crawl","svg-wallpaper","svg-icon"])

    except getopt.GetoptError:
        print(help_str)
        sys.exit(2)

    for opt, arg in opts:

        print(opt, arg)

        if opt in ['-h', '--help']:
            print (help_str)
            sys.exit()
            return

        if opt in ['--data']:
            data_file = arg

        if opt in ['--crawl']:
            settings.crawl = True

        if opt in ['--delete']:
            settings.delete = True

        if opt in ['--new']:
            settings.new_only = True

    current_directory = os.getcwd()


    for opt, arg in opts:
        if opt in ['--svg-wallpaper']:
            svg.export_wallpapers( current_directory, verify=True )
            return

    for opt, arg in opts:
        if opt in ['--svg-icon']:
            svg.export_icons( current_directory, size=256, verify=True )
            return

    if data_file != None:
        if os.path.isfile(data_file):
            data.process( data_file )
            return
        else:
            raise ValueError('could not open ' + data_file)

    # process audio
    audio.process_dir( current_directory, verify=True )

    #svg.process_dir( current_diretory, verify=True)

if __name__ == "__main__":
    main()
