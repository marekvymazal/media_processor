from PIL import Image
import os
import shutil
import subprocess
from sys import platform

from . import settings
from .utilities import get_extensions_in_dir
from .utilities import get_files_with_extensions
from .utilities import should_generate

extensions = [".svg"]

def is_svg( file ):
    if os.path.splitext( file )[1] in extensions:
        return True
    return False

def process( in_file, out_file, ext='jpg', size=(256,256), max=None, quality=95, watermark=None, scale=1 ):

    print(out_file)

    if not should_generate( out_file ):
        return

    # '--export-dpi=200'
    #ln -s /Applications/Inkscape.app/Contents/Resources/bin/inkscape-bin /usr/local/bin/inkscape
    #ln -s /Applications/Inkscape.app/Contents/Resources/script /usr/local/bin/inkscape
    #subprocess.call(['/Applications/Inkscape.app/Contents/Resources/script', '--without-gui', '--export-png=' + out_file, in_file])
    if platform == 'darwin':
        # OS X
        subprocess.call(['/Applications/Inkscape.app/Contents/Resources/script', '--without-gui', '--export-width=' + str(size[0]), '--export-height=' + str(size[1]), '--export-png=' + out_file, in_file])
    elif platform.startswith('linux'):
        # linux
        raise ValueError(platform + ' not currently supported, TODO: add support')
    elif platform == "win32":
        # windows
        raise ValueError(platform + ' not currently supported, TODO: add support')
    else:
        raise ValueError(platform + ' not currently supported, TODO: add support')

    #subprocess.call(['inkscape', '--file=' + in_file, '--export-width=' + str(size[0]), '--export-height=' + str(size[1]), '--export-png=' + out_file])


def export_wallpapers( current_dir, verify=False ):

    wallpaper_sizes = [
        {'name':'720','x':1280,'y':720},
        {'name':'1080','x':1920,'y':1080},
        {'name':'4k','x':3840,'y':2160}
    ]

    #get files
    files = get_files_with_extensions(current_dir, '.svg')
    if len(files) == 0:
        return

    if verify:
        i = input("Convert all .svg to .png wallpapers in " + current_dir + "? (y/n)")
        if i != "y":
            return

    for f in files:
        filename = os.path.splitext(f)[0]
        in_file = os.path.join(current_dir, f)

        for res in wallpaper_sizes:
            out_file = os.path.join(current_dir, filename + '_' + res['name'] + '.png')
            process( in_file, out_file, size=(res['x'], res['y']))

    if settings.crawl:
        #process_dir( )
        pass


def export_icons( current_dir, size=256, verify=False ):

    #wallpaper_sizes = [
    #    {'name':'720','x':1280,'y':720},
    #    {'name':'1080','x':1920,'y':1080},
    #    {'name':'4k','x':3840,'y':2160}
    #]
    sizes = []
    sizes.append(size)

    #get files
    files = get_files_with_extensions(current_dir, '.svg')
    if len(files) == 0:
        return

    if verify:
        i = input("Convert all .svg to .png icons in " + current_dir + "? (y/n)")
        if i != "y":
            return

    for f in files:
        filename = os.path.splitext(f)[0]
        in_file = os.path.join(current_dir, f)

        for res in sizes:
            out_file = os.path.join(current_dir, filename + '.png')
            process( in_file, out_file, size=(res, res))

    if settings.crawl:
        #process_dir( )
        pass
