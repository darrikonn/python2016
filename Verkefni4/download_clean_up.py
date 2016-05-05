#!/usr/bin/env python
import argparse, re, os, sys, json, logging

# keep a global LOG of all crucial changes
logging.basicConfig(level=logging.INFO,
        filename='info_logger.log',
        filemode='a',
        format='%(asctime)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')
LOGGER = logging.getLogger('info_logger')

def move_files(filename, destination):
    try:
        if os.path.exists(filename):
            os.rename(filename, destination)
            LOGGER.info(': File MOVED!:\n{0} -> {1}\n'.format(filename, destination))
    except:
        sys.stderr.write('Could not rename/move {0} to {1}'.format(filename, destination))

def create_directories(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except:
        sys.stderr.write('Could not create directory {0}'.format(directory))

def remove_directory(directory):
    if os.path.isdir(directory):
        try:
            if os.listdir(directory) == []:
                os.rmdir(directory)
        except:
            sys.stderr.write('Could not remove the directory {0}'.format(directory))

def remove_file(filename):
    try:
        if os.path.exists(filename):
            os.remove(filename)
            LOGGER.info(': File REMOVED!:\n{0}\n'.format(filename))
    except:
        sys.stderr.write('Could not remove file {0}'.format(filename))

#
# get the user configurations from the config file
#
def get_configurations(PATH):
    try:
        with open(PATH) as cf:
            items = json.loads(cf.read())
            return {'NonValid': items['NonValidFileExtensions'],
                    'Subtitles': items['ValidSubtitleFileExtensions'],
                    'Books': items['ValidBookFileExtensions'],
                    'Exclude': items['ExcludeDirectories'],
                    'Video': items['ValidVideoFileExtensions'],
                    'KnownShows': items['KnownTVShows'],
                    'Songs': items['ValidSongFileExtensions']}
    except:
        sys.stderr.write('Could not open the configuration file, or json file not valid\n')

#
# get all known shows that the user specified in the config file
#
def is_a_known_show(f, keys):
    folder = [x for x in keys if x.title() in f.title()]
    if not folder:
        return []
    else:
        return folder[0]

#
# create title of the folder being created
#
def get_title(f):
    return ' '.join(f[:f.rfind('.')].split('.')).strip().title()

def check_file_extension(f, keys):
    return any(f for x in keys if f.endswith(x))

def check_file_start(f, path, keys):
    return any(f for x in keys if f.startswith(os.path.join(path, x)))

#
# initialize the downloads directory with few root directories
#
def initialize(ROOT):
    create_directories(os.path.join(ROOT, 'Movies'))
    create_directories(os.path.join(ROOT, 'Songs'))
    create_directories(os.path.join(ROOT, 'Books'))
    create_directories(os.path.join(ROOT, 'TV-Shows'))
    create_directories(os.path.join(ROOT, 'Other (Unsorted)'))

#
# sort the files and clean up the downloads directory
#
def sort_files(args):
    TV_RE = r'(.*)(?:s|season| |\[)( ?\d+)(?: *?| ?-? ?)(?:e|episode|x)( ?\d+)'
    TV_CRE = re.compile(TV_RE, re.I)
    config = get_configurations(args.config_filename)
    initialize(args.filename)
    ROOT = args.filename[args.filename.rfind('/'):]
    for root, dirs, files in os.walk(args.filename, topdown=False):
        if check_file_start(root, args.filename, config['Exclude']):
            continue
        for f in files:
            tv_show = TV_CRE.findall(' '.join(f.split('.')))
            path = os.path.join(root, f)
            old_parent_folder = re.sub(args.filename + '/', '', path)
            index = old_parent_folder.find('/')
            if index == -1:
                index = len(old_parent_folder)
            old_parent_folder = old_parent_folder[:index]
            known_show = is_a_known_show(old_parent_folder, config['KnownShows'])
            if check_file_extension(f, config['NonValid']):
                # delete non valid files
                remove_file(path)
            elif not known_show == []:
                # if the show is in the config file, then it is easier to clean up
                parent_folder = '{0}{1}'.format('TV-Shows/', known_show)
                create_directories(os.path.join(args.filename, parent_folder))
                new_path = os.path.join(args.filename, parent_folder)
                if os.listdir(new_path) == []:
                    move_files(os.path.join(args.filename, old_parent_folder),
                            new_path)
                else:
                    move_files(os.path.join(args.filename, old_parent_folder),
                            new_path + '/' + old_parent_folder)
            elif tv_show:
                # check first if we can sort tv shows from a pattern of (seasons/episodes)
                top_folder = 'TV-Shows/'
                if check_file_extension(f, config['Songs']):
                    top_folder = 'Songs/'
                parent_folder = '{0}{1}{2}{3}'.format(top_folder,
                        ' '.join(tv_show[0][0].split('.')).strip().title(),
                        '/Season ' + str(int(tv_show[0][1])),
                        '/Episode ' + str(int(tv_show[0][2])))
                # add the subtitles to a subtitle directory for the show
                if check_file_extension(f, config['Subtitles']):
                    parent_folder = '{0}/Subtitles'.format(parent_folder)
                create_directories(os.path.join(args.filename, parent_folder))
                move_files(path, os.path.join(args.filename, parent_folder + '/' + f))
            elif check_file_extension(f, config['Songs']):
                parent_folder = root[root.rfind(ROOT)+len(ROOT):]
                if parent_folder == '':
                    parent_folder = get_title(f)
                parent_folder = 'Songs/{0}'.format(parent_folder)
                create_directories(os.path.join(args.filename, parent_folder))
                move_files(path, os.path.join(args.filename, parent_folder + '/' + f))
            elif check_file_extension(f, config['Subtitles']):
                parent_folder = '{0}{1}{2}'.format('Movies/', get_title(f), '/Subtitles')
                create_directories(os.path.join(args.filename, parent_folder))
                move_files(path, os.path.join(args.filename, parent_folder + '/' + f))
            elif check_file_extension(f, config['Books']):
                parent_folder = '{0}{1}'.format('Books/', get_title(f))
                create_directories(os.path.join(args.filename, parent_folder))
                move_files(path, os.path.join(args.filename, parent_folder + '/' + f))
            elif check_file_extension(f, config['Video']):
                parent_folder = '{0}{1}'.format('Movies/', get_title(f))
                create_directories(os.path.join(args.filename, parent_folder))
                move_files(path, os.path.join(args.filename, parent_folder + '/' + f))
            else:
                # if we can't find a pattern to sort, add to the Other (unsorted) directory
                parent_folder = '{0}{1}'.format('Other (Unsorted)/', get_title(f))
                create_directories(os.path.join(args.filename, parent_folder))
                move_files(path, os.path.join(args.filename, parent_folder + '/' + f))

        for d in dirs:
            # remove all empty directories
            remove_directory(os.path.join(root, d))

#
# need to validate input files from the user
#
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
        move_files(os.path.dirname(os.path.realpath(__file__)) + '/info_logger.log',
                args.filename + '/info_logger.log')
        print('Succeeded!')
    except:
        sys.stderr.write('Error while cleaning up the downloads directory!')

if __name__ == '__main__':
    sys.exit(main())
