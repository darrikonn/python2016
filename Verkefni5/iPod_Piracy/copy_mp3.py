#!/usr/bin/env python
import argparse, stagger, os, sys

def create_directories(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except:
        sys.stderr.write('Could not create directory {0}\n'.format(directory))

def move_files(filename, destination):
    try:
        if os.path.exists(filename):
            os.rename(filename, destination)
    except:
        sys.stderr.write('Could not rename/move {0} to {1}\n'.format(filename, destination))

def _get_title(info):
    return '{0} - {1}'.format(info.track, info.title)

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
    other_folder = os.path.join(os.getcwd(), 'Other')
    _initialize(args.targetname, other_folder)
    for root, dirs, files in os.walk(args.filename):
        for f in files:
            path = os.path.join(root, f)
            try:
                info = stagger.read_tag(path)
                artist = os.path.join(targetname, info.artist)
                album = os.path.join(artist, info.album)
                _structure_parent_folder(artist, album)
                move_files(path, os.path.join(album, _get_title(info)))
            except NoTagError:
                # file too short
                move_files(path, os.path.join(other_folder, f))
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
        sys.stderr.write('Error while copying mp3 files to target folder')

if __name__ == '__main__':
    sys.exit(main())
