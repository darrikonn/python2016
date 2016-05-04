#!/usr/bin/env python
import argparse, re, os, sys, json

def re_type(s):
    try:
        re.compile(s)
    except:
        raise argparse.ArgumentTypeError('Invalid regex')
    return s

def move_files(filename, destination):
    if os.path.exists(filename):
        os.rename(filename, destination)

def create_directories(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def initialize(ROOT):
    create_directories(os.path.join(ROOT, 'Movies'))
    create_directories(os.path.join(ROOT, 'Songs'))
    create_directories(os.path.join(ROOT, 'Books'))
    create_directories(os.path.join(ROOT, 'TV-Shows'))
    create_directories(os.path.join(ROOT, 'Other (unsorted)'))

def remove_file(filename):
    if os.path.isdir(filename):
        try:
            os.rmdir(filename)
        except:
            sys.stderr.write('Could not remove the directory %s' % filename)
    else:
        try:
            if os.path.exists(filename):
                os.remove(filename)
        except:
            sys.stderr.write('Could not remove file %s' % filename)

def get_configurations(PATH):
    with open(PATH) as cf:
        items = json.loads(cf.read())
        return {'NonValid': items['NonValidFileExtensions'],
                'Subtitles': items['ValidSubtitleFileExtensions'],
                'Books': items['ValidBookFileExtensions'],
                'Songs': items['ValidSongFileExtensions']}


def clean_up(args):
    TV_RE = '(.*)\.s(\d*)e(\d*)'
    #TV_CRE = re.compile(TV_RE)
    config = get_configurations(args.config_filename)
    initialize(args.filename)
    for root, dirs, files in os.walk(args.filename):
        for f in files:
            tv_show = re.findall(TV_RE, f, re.I)
            path = os.path.join(root, f)
            print(os.path.join(args.filename, f))
            if any(f for x in config['NonValid'] if f.endswith(x)):
                # delete file and continue
                remove_file(path)
            elif tv_show:
                parent_folder = '{0}{1}{2}{3}'.format('TV-Shows/',
                        ' '.join(tv_show[0][0].split(',')).title(),
                        '/Season ' + tv_show[0][1], '/Episode ' + tv_show[0][2])
                create_directories(os.path.join(args.filename, parent_folder))
                #move_files(path, parent_folder + '/' + f)

    return None

def validate_file(parser, filepath):
    if os.path.exists(filepath):
        return filepath
    else:
        return parser.error('The file/directory "%s" does not exist!' % filepath)

def main():
    parser = argparse.ArgumentParser(description='Download clean up')
    parser.add_argument('-i', '--input', dest='filename', required=True,
                    help='The source of the downloads directory.', metavar='FILE',
                    type=lambda f: validate_file(parser, f))
    parser.add_argument('-c', '--config', dest='config_filename', required=True,
                    help='Configuration file that helps cleaning up the downloads directory',
                    metavar='FILE', type=lambda f: validate_file(parser, f))

    args = parser.parse_args()
    clean_up(args)

if __name__ == '__main__':
    sys.exit(main())
