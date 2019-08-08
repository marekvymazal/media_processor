import os

from . import settings

def get_extensions_in_dir( directory ):

    exts = set()

    files = os.listdir(directory)
    for f in files:
        ext = os.path.splitext(f)[1]
        if ext != None and len(ext) > 0:
            exts.add(ext)

    return exts

def get_files_with_extensions(directory, *exts):
    """
    gets files in directory with specific extensions
    """

    print(exts)

    found = []

    files = os.listdir(directory)
    for f in files:
        ext = os.path.splitext(f)[1]
        if ext in exts:
            found.append(f)

    return found


def should_generate( out_file ):
    if not settings.new_only or (settings.new_only and not os.path.isfile(out_file)):
        return True
    return False


def purify( folder_targets ):

    for item in folder_targets:

        def proc( cur_folder, main_files ):

            found_file = False

            files = os.listdir( cur_folder )
            for f in files:
                if f.startswith('.'):
                    continue

                fp = os.path.join( cur_folder, f)
                if os.path.isdir(fp):
                    found = proc( fp, main_files )
                    if found:
                        found_file = True
                    else:
                        #print('del folder:' + fp)
                        os.rmdir(fp)

                elif fp in main_files:
                    found_file = True
                else:
                    #print("del:" + fp)
                    os.remove(fp)

            return found_file


        root = folder_targets[item]['root']

        proc( root, folder_targets[item]['files'] )
