from PIL import Image
import os
import shutil

from . import settings
from .utilities import should_generate

extensions = [".jpg", ".png", ".bmp", ".tga", ".tif"]

def is_image( file ):
    if os.path.splitext( file )[1] in extensions:
        return True
    return False

def process( in_file, out_file, ext='jpg', max=None, quality=95, watermark=None, scale=1 ):

    if not should_generate( out_file ):
        return

    padding = 10 # for watermark border

    i = Image.open(in_file)

    # setup
    wm = None
    if watermark != None and is_image(watermark):
        wm = Image.open(watermark)

    count = 0

    # get image sizes
    baseW, baseH = i.size

    wmW, wmH = [0,0]
    if wm != None:
        wmW, wmH = wm.size

    # get percent to scale
    percent = 1.0

    if scale != 1.0:
        percent = scale

    if max != None:
        if baseW > max[0]:
            percent = float(max[0]) / float(baseW)

        if baseH > max[1]:
            percentH = float(max[1]) / float(baseH)
            if percentH < percent:
                percent = percentH

    # scale image
    if percent != 1.0:
        w = int(float(percent)*float(baseW))
        h = int(float(percent)*float(baseH))
        i = i.resize((w, h), Image.ANTIALIAS)

    waterW, waterH = i.size
    if wm != None:
        i.paste(wm, (waterW-wmW-padding, waterH-wmH-padding), wm)

    i = i.convert("RGB")
    i.save(out_file, quality=quality, optimize=True, progressive=True)
    i.close()

    if wm != None:
        wm.close()
