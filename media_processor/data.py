import os
import shutil
from bs4 import BeautifulSoup

from . import settings
from . import utilities

from . import image
from . import gif
from . import audio
from . import video

def process( data_file ):

     # folders that are exported to
    #file_targets = [] # files that are intended to be exported to said folders

    data_str = open(data_file, 'r')
    #data = BeautifulSoup(data_str, "html5lib").contents[0].contents[1].contents[0]
    data = BeautifulSoup(data_str, "xml").contents[0] # this respects self closing tags
    data_str.close()

    if data.has_attr('debug'):
        debug = data['debug'] == 'True'
        print("debug:" + str(debug))

    raw_folder = None
    target_folder = None

    if data.has_attr('raw'):
        raw_folder = data['raw']

    if data.has_attr('target'):
        target_folder = data['target']
    else:
        raise ValueError('No target specified')

    if data.has_attr('watermark'):
        settings.watermark = data['watermark']

    print("raw:", raw_folder)
    print("target:", target_folder)
    print("watermark:", settings.watermark)

    target_folders = {}

    target_folders['galleries'] = {}
    target_folders['galleries']['root']=os.path.join(target_folder,'galleries')
    target_folders['galleries']['dir'] = set()
    target_folders['galleries']['files'] = []

    target_folders['thumbnails'] = {}
    target_folders['thumbnails']['root']=os.path.join(target_folder,'thumbnails')
    target_folders['thumbnails']['dir'] = set()
    target_folders['thumbnails']['files'] = []

    target_folders['images'] = {}
    target_folders['images']['root']=os.path.join(target_folder,'images')
    target_folders['images']['dir'] = set()
    target_folders['images']['files'] = []

    target_folders['gifs'] = {}
    target_folders['gifs']['root']=os.path.join(target_folder,'gifs')
    target_folders['gifs']['dir'] = set()
    target_folders['gifs']['files'] = []

    target_folders['video'] = {}
    target_folders['video']['root']=os.path.join(target_folder,'video')
    target_folders['video']['dir'] = set()
    target_folders['video']['files'] = []

    target_folders['music'] = {}
    target_folders['music']['root']=os.path.join(target_folder,'music')
    target_folders['music']['dir'] = set()
    target_folders['music']['files'] = []

    # process galleries
    galleries_tags = data.find_all('galleries')
    for galleries in galleries_tags:
        for gallery in galleries:
            if gallery.name != 'gallery':
                continue

            images = []

            try:
                name = gallery['name']
            except:
                raise ValueError('No name specified for gallery')

            print(name)

            # get images
            for i in gallery:
                if i.name != 'image':
                    continue

                try:
                    src = i['src']
                    f = os.path.join( raw_folder, src )
                    if image.is_image(f):
                        images.append(f)
                except:
                    src = None

            # get images for folder
            try:
                folder = os.path.join(raw_folder, gallery['folder'])
                for f in os.listdir(folder):
                    if image.is_image(f):
                        images.append(os.path.join(folder,f))
            except:
                folder = None

            # process gallery
            gallery_target = os.path.join(target_folder, 'galleries', name )
            target_folders['galleries']['dir'].add(gallery_target)
            if not os.path.exists(gallery_target):
                os.makedirs(gallery_target)

            thumbnail_target = os.path.join(target_folder, 'thumbnails', name )
            target_folders['thumbnails']['dir'].add(thumbnail_target)
            if not os.path.exists(thumbnail_target):
                os.makedirs(thumbnail_target)

            cnt = 1
            for i in images:
                print('  ', i)

                basename = os.path.basename( i )
                filename, ext = os.path.splitext( basename )

                # process web
                out_file = os.path.join( gallery_target, name + '-' + str(cnt) + '.jpg' )
                target_folders['galleries']['files'].append(out_file)

                image.process( i, out_file, ext='jpg', max=(800,600), quality=95, watermark=settings.watermark)

                # process thumbnail
                out_file = os.path.join( thumbnail_target, name + '-' + str(cnt) + '-thumbnail.jpg' )
                target_folders['thumbnails']['files'].append(out_file)
                image.process( i, out_file, ext='jpg', max=(105,140), quality=95)

                cnt += 1


    # process images
    images_tags = data.find_all('images')
    for images in images_tags:
        for tag in images:
            if tag.name != 'file':
                continue

            scale = 1.0
            try:
                scale = float(tag['scale'])
            except:
                pass

            try:
                src = tag['src']
            except:
                raise ValueError('No src specified for image')

            try:
                target = tag['target']
            except:
                raise ValueError('No target specified for image')

            # tag use watermark override
            cur_watermark = None
            try:
                if tag['use_watermark'].lower() == 'true':
                    cur_watermark = settings.watermark
                elif tag['use_watermark'].lower() == 'false':
                    cur_watermark = None

            except:
                pass

            image_rel, filename = os.path.split( target )

            # process folder
            image_folder = os.path.join(target_folder, 'images', image_rel )
            target_folders['images']['dir'].add(image_folder)
            if not os.path.exists(image_folder):
                os.makedirs(image_folder)

            # process web
            in_file = os.path.join( raw_folder, src )
            out_file = os.path.join( image_folder, filename + '.jpg' )

            target_folders['images']['files'].append(out_file)

            image.process( in_file, out_file, ext='jpg', quality=95, scale=scale, watermark=cur_watermark)

            print( filename )
            print('  ' + in_file)
            print('  ' + out_file)




    # process videos
    videos_tags = data.find_all('videos')
    for videos in videos_tags:

        # group usewatermark override
        vid_watermark = settings.watermark
        try:
            if videos['use_watermark'].lower() == 'false':
                vid_watermark = None
        except:
            pass

        for tag in videos:
            if tag.name != 'file':
                continue

            try:
                src = tag['src']
            except:
                raise ValueError('No src specified for video')

            try:
                target = tag['target']
            except:
                raise ValueError('No target specified for video')

            # tag use watermark override
            cur_watermark = vid_watermark
            try:
                if tag['use_watermark'].lower() == 'true':
                    cur_watermark = settings.watermark
                elif tag['use_watermark'].lower() == 'false':
                    cur_watermark = None

            except:
                pass

            video_rel, filename = os.path.split( target )

            # process folder
            video_folder = os.path.join(target_folder, 'video', video_rel )
            target_folders['video']['dir'].add(video_folder)
            if not os.path.exists(video_folder):
                os.makedirs(video_folder)

            in_file = os.path.join( raw_folder, src )
            out_file = os.path.join( video_folder, filename + '.mp4' )
            out_image = os.path.join( video_folder, filename + '.jpg' )

            target_folders['video']['files'].append(out_file)
            target_folders['video']['files'].append(out_image)

            video.process( in_file, out_file, out_image, watermark=cur_watermark )

            print( filename )
            print('  ' + in_file)
            print('  ' + out_file)
            print('  ' + out_image)


    # process gifs
    gifs_tags = data.find_all('gifs')
    for gifs in gifs_tags:
        for tag in gifs:
            if tag.name != 'file':
                continue

            try:
                src = tag['src']
            except:
                raise ValueError('No src specified for gif')

            try:
                target = tag['target']
            except:
                raise ValueError('No target specified for gif')

            try:
                scale = tag['scale']
            except:
                scale = None

            try:
                crop_x = tag['crop_x']
            except:
                crop_x = None

            try:
                crop_y = tag['crop_y']
            except:
                crop_y = None

            try:
                crop_w = tag['crop_w']
            except:
                crop_w = None

            try:
                crop_h = tag['crop_h']
            except:
                crop_h = None

            try:
                start_time = tag['start_time']
            except:
                start_time = None

            try:
                end_time = tag['end_time']
            except:
                end_time = None

            gif_rel, filename = os.path.split( target )

            # process folder
            gif_folder = os.path.join(target_folder, 'gifs', gif_rel )
            target_folders['gifs']['dir'].add(gif_folder)
            if not os.path.exists(gif_folder):
                os.makedirs(gif_folder)

            # process web
            in_file = os.path.join( raw_folder, src )
            out_file = os.path.join( gif_folder, filename + '.gif' )

            target_folders['gifs']['files'].append(out_file)

            gif.process( in_file, out_file, scale=scale, crop_x=crop_x, crop_y=crop_y, crop_w=crop_w, crop_h=crop_h, start_time=start_time, end_time=end_time )

            print( filename )
            print('  ' + in_file)
            print('  ' + out_file)



    # process music
    musics_tags = data.find_all('music')
    for music in musics_tags:
        for tag in music:
            if tag.name != 'file':
                continue

            try:
                src = tag['src']
            except:
                raise ValueError('No src specified for music')

            try:
                target = tag['target']
            except:
                raise ValueError('No target specified for music')


            music_rel, filename = os.path.split( target )

            # process folder
            music_folder = os.path.join(target_folder, 'music', music_rel )
            target_folders['music']['dir'].add(music_folder)
            if not os.path.exists(music_folder):
                os.makedirs(music_folder)

            # process web
            in_file = os.path.join( raw_folder, src )
            out_file = os.path.join( music_folder, filename + '.mp3' )

            target_folders['music']['files'].append(out_file)

            audio.process( in_file, out_file )

            print( filename )
            print('  ' + in_file)
            print('  ' + out_file)

    if settings.delete:
        utilities.purify( target_folders )
