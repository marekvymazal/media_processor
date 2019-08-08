import os
import shutil

from . import settings
from .utilities import should_generate

def process( in_file, out_file, out_image, watermark=None, padding=5 ):

    if should_generate( out_file ):
        if os.path.splitext( in_file )[1] == '.mp4' and watermark == None:
            # just copy video over
            try:
                shutil.copyfile( in_file, out_file )
            except:
                raise ValueError('could not copy ' + in_file)
        else:

            if watermark != None:
                #ffmpeg -i input.mp4 -i logo.png -filter_complex \
                #"overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2" \
                #-codec:a copy output.mp4
                vs = '"overlay=(main_w-overlay_w)-' + str(padding) + ':(main_h-overlay_h)-' + str(padding) + '"'
                os.system('ffmpeg -i "' + in_file + '" -i "' + watermark + '" -filter_complex ' + vs + ' -y "' + out_file + '"')
            else:
                # process web
                os.system('ffmpeg -i "' + in_file + '" -y "' + out_file + '"')

    # create static image
    # -vf "select=eq(n\,1) :gets the first frame
    # -q:v 3 :sets the quality to 3
    # -y :forces overwrite, so script isn't disturpted
    if should_generate( out_image ):
        if watermark != None:
            #vs = '"overlay=(main_w-overlay_w)-' + str(padding) + ':(main_h-overlay_h)-' + str(padding) + '"'
            #os.system('ffmpeg -i "' + in_file + '" -i "' + watermark + '" -filter_complex ' + vs + ' -q:v 3 -vframes 1 -y "' + out_image + '"')

            vs = '"select=eq(n\,1),overlay=(main_w-overlay_w)-' + str(padding) + ':(main_h-overlay_h)-' + str(padding) + '"'
            os.system('ffmpeg -i "' + in_file + '" -i "' + watermark + '" -filter_complex ' + vs + ' -q:v 3 -y "' + out_image + '"')
            #ffmpeg -i movie.mp4 -i image.png
            #   -filter_complex
            #           "[0]scale=W:H:force_original_aspect_ratio=decrease[v];
            #            [v][1]overlay=(W-w)/2:(H-h)/2"
            #  -vframes 1  output.jpg
        else:
            os.system('ffmpeg -i "' + in_file + '" -vf "select=eq(n\,1)" -q:v 3 -y "' + out_image + '"')
