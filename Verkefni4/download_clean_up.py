#!/usr/bin/env python
import argparse, re, os, sys, json

def re_type(s):
    try:
        re.compile(s)
    except:
        raise argparse.ArgumentTypeError('Invalid regex')
    return s

def move_files(filename, destination):
    try:
        if os.path.exists(filename):
            os.rename(filename, destination)
    except:
        sys.stderr.write('Could not rename/move {0} to {1}'.format(filename, directory))

def create_directories(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except:
        sys.stderr.write('Could not create directory {0}'.format(directory))

def initialize(ROOT):
    create_directories(os.path.join(ROOT, 'Movies'))
    create_directories(os.path.join(ROOT, 'Songs'))
    create_directories(os.path.join(ROOT, 'Books'))
    create_directories(os.path.join(ROOT, 'TV-Shows'))
    create_directories(os.path.join(ROOT, 'Other (unsorted)'))

def remove_file(filename):
    if os.path.isdir(filename):
        try:
            if os.listdir(filename) == []:
                os.rmdir(filename)
        except:
            sys.stderr.write('Could not remove the directory {0}'.format(filename))
    else:
        try:
            if os.path.exists(filename):
                os.remove(filename)
        except:
            sys.stderr.write('Could not remove file {0}'.format(filename))

def get_configurations(PATH):
    with open(PATH) as cf:
        items = json.loads(cf.read())
        return {'NonValid': items['NonValidFileExtensions'],
                'Subtitles': items['ValidSubtitleFileExtensions'],
                'Books': items['ValidBookFileExtensions'],
                'Exclude': items['ExcludeDirectories'],
                'Songs': items['ValidSongFileExtensions']}


def clean_up(args):
    TV_RE = r'(.*)(?: ?s ?| ?season ?| ?\[ ?|\.)(\d+)(?: ?e ?| ?episode ?| ?x ?)(\d+)'
    TV_CRE = re.compile(TV_RE, re.I)
    config = get_configurations(args.config_filename)
    initialize(args.filename)
    for root, dirs, files in os.walk(args.filename):
        for f in files:
            tv_show = TV_CRE.findall(f)
            path = os.path.join(root, f)
            if any(f for x in config['NonValid'] if f.endswith(x)):
                # delete file and continue
                remove_file(path)
            elif tv_show:
                parent_folder = '{0}{1}{2}{3}'.format('TV-Shows/',
                        ' '.join(tv_show[0][0].split('.')).strip().title(),
                        '/Season ' + str(int(tv_show[0][1])),
                        '/Episode ' + str(int(tv_show[0][2])))
                create_directories(os.path.join(args.filename, parent_folder))
                move_files(path, os.path.join(args.filename, parent_folder + '/' + f))
        # directory gets deleted if it's empty
        remove_file(root)

def validate_file(parser, filepath):
    if os.path.exists(filepath):
        return filepath
    else:
        return parser.error('The file/directory "{0}" does not exist!'.format(filepath))

def main():
    parser = argparse.ArgumentParser(description='This application will clean up your download directory!')
    parser.add_argument('-i', '--input', dest='filename', required=True,
                    help='The source of the downloads directory.', metavar='FILE',
                    type=lambda f: validate_file(parser, f))
    parser.add_argument('-c', '--config', dest='config_filename', required=True,
                    help='Configuration file that helps cleaning up the downloads directory',
                    metavar='FILE', type=lambda f: validate_file(parser, f))

    args = parser.parse_args()

    # use the absolute path of the files
    args.filename = os.path.abspath(args.filename)
    args.config_filename = os.path.abspath(args.config_filename)

    print('Processing...')
    try:
        clean_up(args)
        print('Succeeded!')
    except:
        sys.stderr.write('Error while cleaning up the downloads directory!')

if __name__ == '__main__':
    sys.exit(main())
