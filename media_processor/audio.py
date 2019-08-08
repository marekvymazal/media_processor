import os

from . import settings

from .utilities import get_extensions_in_dir
from .utilities import get_files_with_extensions
from .utilities import should_generate

def process_dir( current_dir, verify=False ):

    files = get_files_with_extensions(current_dir, '.wav')
    if len(files) == 0:
        return

    if verify:
        i = input("Convert all .wav to mp3 in " + current_dir + "? (y/n)")
        if i != "y":
            return

    for f in files:
        filename = os.path.splitext(f)[0]
        in_file = os.path.join(current_dir, f)
        out_file = os.path.join(current_dir, filename + '.mp3')
        process( in_file, out_file )

    if settings.crawl:
        #process_dir( )
        pass


def process( in_file, out_file ):
    if not should_generate( out_file ):
        return

    os.system('ffmpeg -i ' + in_file + ' -qscale:a 0 -y ' + out_file)
