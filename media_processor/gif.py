"""
settings
    scale= final output width, if None then it will use crop_w, if both are None then it will use original
    crop_x/crop_y=top left corner of crop
    crop_w/crop_h=width and height of crop from top left corner

    start_time=seconds into video gif should start
    end_time=seconds into video gif should end
"""

#uses PIL libraries
from PIL import Image
import os
import shutil

from . import settings
from .utilities import should_generate

def process( in_file, out_file, scale=None, crop_x=None, crop_y=None, crop_w=None, crop_h=None, start_time=None, end_time=None):

    if not should_generate( out_file ):
        return

    #output_resolution = str(640)
    palette_file = os.path.splitext( out_file )[0] + '.png'

    if scale != None:
        scale = scale + ':-1'
    if scale == None and crop_w != None:
        scale = crop_w + ':-1'
    if scale == None:
        scale = 'iw:ih'

    #-ss 15 -t 20
    duration = None
    if end_time != None:
        duration = float(end_time)
    if start_time != None and end_time != None:
        duration = float(end_time) - float(start_time)

    filters = ''
    filters += 'fps=15'
    filters += ',scale=' + str(scale)
    filters += ':flags=lanczos'

    '''
     -ss start_time
     -t duration
    '''
    #print (in_file)
    #print (out_file)
    print (palette_file)

    # export palette
    os.system('ffmpeg -i "' + in_file + '" -vf palettegen -y "' + palette_file + '"')


    extra_settings = ''
    extra_settings += 'fps=15'

    if crop_w is not None and crop_h is not None and crop_x is not None and crop_y is not None:
        extra_settings += ',crop=' + crop_w + ':' + crop_h + ':' + crop_x + ':' + crop_y

    extra_settings += ',scale=' + str(scale) + ':flags=lanczos[x];[x][1:v]paletteuse'

    ranges = ''
    if start_time != None:
        ranges += '-ss ' + start_time
    if duration != None:
        ranges += ' -t ' + str(duration)

    os.system('ffmpeg -i "' + in_file + '" -i "' + palette_file + '" -lavfi "' + extra_settings + '" ' + ranges +' -y "' + out_file + '"')
    #ffmpeg -i "${1}" -i "${1}.png" -filter_complex "fps=${3:-10},scale=${2:-320}:-1:flags=lanczos[x];[x][1:v]paletteuse" "${1}".gif

    """
    palette="/tmp/palette.png"
    filters="fps=15,scale=320:-1:flags=lanczos"

    ffmpeg -i input.flv -vf "$filters,palettegen" -y $palette
    ffmpeg -i input.flv -i $palette -lavfi "$filters [x]; [x][1:v] paletteuse" -y output.gif
    """

    os.remove( palette_file )
