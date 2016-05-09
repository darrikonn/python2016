#!/usr/bin/env python
import argparse, stagger, os, sys, shutil, traceback

def create_directories(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except:
        sys.stderr.write('Could not create directory {0}\n'.format(directory))

def copy_files(src, dest):
    try:
        if os.path.exists(src):
            shutil.copyfile(src, dest)
    except:
        sys.stderr.write('Could not copy {0} to {1}\n'.format(src, dest))
#
# return the title of the song, with track number if it exists
#
def _get_title(info):
    title = info.title.replace('/', '|')
    if info.track == 0:
        return title
    return '{0} - {1}'.format(info.track, title)

def _structure_parent_folder(artist, album):
    try:
        create_directories(artist)
        create_directories(album)
    except:
        sys.stderr.write('Could not structure parent folder!\n')

def _initialize(targetname, other_folder):
    create_directories(targetname)
    create_directories(other_folder)

def _copy_files(args):
    other_folder = os.path.join(args.targetname, 'Other')
    _initialize(args.targetname, other_folder)
    for root, dirs, files in os.walk(args.filename):
        for f in files:
            path = os.path.join(root, f)
            try:
                info = stagger.read_tag(path)
                # copy to the other folder if the title or the artist is unknown
                if info.artist == '' or info.title == '':
                    raise stagger.NoTagError
                artist = os.path.join(args.targetname, info.artist)
                album = os.path.join(artist, info.album)
                _structure_parent_folder(artist, album)
                copy_files(path, os.path.join(album, _get_title(info)))
            except stagger.NoTagError:
                # file too short
                copy_files(path, os.path.join(other_folder, f))
            except:
                sys.stderr.write('Can\'t use stagger to read tag of {0}\n'.format(path))

def validate_directory(parser, directory):
    if os.path.exists(directory) and os.path.isdir(directory):
        return directory
    else:
        return parser.error('The directory "{0}" does not exist!'.format(directory))

def main():
    parser = argparse.ArgumentParser(description='A Python script that copies the music files from iPod\'s hard drive into another directory')
    parser.add_argument('-i', '--input', dest='filename', required=True,
            help='The source directory of the iPod\'s hard drive', metavar='FILE',
            type=lambda f: validate_directory(parser, f))
    parser.add_argument('-o', '--output', dest='targetname', required=True,
            help='The target directory of the iPod\'s hard drive', metavar='FILE')

    args = parser.parse_args()

    # use the absolute path of the directories
    args.filename = os.path.abspath(args.filename)
    args.targetname = os.path.join(os.getcwd(), args.targetname)

    print('Processing...')
    try:
        _copy_files(args)
        print('Succeeded!')
    except:
        traceback.print_exc()
        sys.stderr.write('Error while copying mp3 files to target folder')

if __name__ == '__main__':
    sys.exit(main())
