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

def remove_directory(directory):
    if os.path.isdir(filename):
        try:
            if os.listdir(filename) == []:
                os.rmdir(filename)
        except:
            sys.stderr.write('Could not remove the directory {0}'.format(filename))

def remove_file(filename):
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
                'Video': items['ValidVideoFileExtensions'],
                'Songs': items['ValidSongFileExtensions']}

def check_file_extension(f, key):
    return any(f for x in key if f.endswith(x))

def sort_files(args):
    TV_RE = r'(.*)(?: ?s ?| ?season ?| ?\[ ?|\.)(\d+)(?: ?e ?| ?episode ?| ?x ?)(\d+)'
    TV_CRE = re.compile(TV_RE, re.I)
    config = get_configurations(args.config_filename)
    initialize(args.filename)
    for root, dirs, files in os.walk(args.filename, topdown=False):
        for f in files:
            tv_show = TV_CRE.findall(f)
            path = os.path.join(root, f)
            #print(os.path.dirname(path))
            if check_file_extension(f, config['NonValid']):
                # delete file and continue
                remove_file(path)
            elif check_file_extension(f, config['Songs']):
                parent_folder = '{0}{1}'.format('Songs/',
                        ' '.join(f[:f.rfind('.')].split('.')).strip())
                create_directories(os.path.join(args.filename, parent_folder))
                move_files(path, os.path.join(args.filename, parent_folder + '/' + f))
            elif tv_show:
                parent_folder = '{0}{1}{2}{3}'.format('TV-Shows/',
                        ' '.join(tv_show[0][0].split('.')).strip().title(),
                        '/Season ' + str(int(tv_show[0][1])),
                        '/Episode ' + str(int(tv_show[0][2])))
                create_directories(os.path.join(args.filename, parent_folder))
                move_files(path, os.path.join(args.filename, parent_folder + '/' + f))
            elif check_file_extension(f, config['Video']):
                parent_folder = '{0}{1}'.format('Movies/',
                        ' '.join(f[:f.rfind('.')].split('.')).strip())
                create_directories(os.path.join(args.filename, parent_folder))
                move_files(path, os.path.join(args.filename, parent_folder + '/' + f))
            else:
                parent_folder = '{0}{1}'.format('Other (unsorted)/',
                        ' '.join(f[:f.rfind('.')].split('.')).strip())
                create_directories(os.path.join(args.filename, parent_folder))
                move_files(path, os.path.join(args.filename, parent_folder + '/' + f))

        if root == args.filename:
            for d in dirs:
                remove_directory(d)

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
        sort_files(args)
        print('Succeeded!')
    except:
        sys.stderr.write('Error while cleaning up the downloads directory!')

if __name__ == '__main__':
    sys.exit(main())
