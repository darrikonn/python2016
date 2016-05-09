This is a python3 application that sorts your downloads directory. You should run this app in a shell with two flags, i.e. -i (or --input) which is the downloads directory (full path not needed) and -c (or --config) which is a json config file that helps the sorting.
e.g.:
./download_clean_up.py -i downloads/ -c config.json

You are provided with a default config.json file that has the following attributes:
"NonValidFileExtensions" -> this will be file extensions that should be removed (Warning zone)
"ValidSubtitleFileExtensions" -> these are the file extensions of your subtitles
"ValidBookFileExtensions" -> all valid book file extensions
"ValidSongFileExtensions" -> all valid song file extensions
"ValidVideoFileExtensions" -> all valid video file extensions
"ExcludeDirectories" -> these are the private directories that should not be sorted
"KnownTVShows" -> this will help the application to sort your files based on known TV-Shows. Feel free to add your TV-Shows (not necessary).

No PyPI packages are needed, nor other dependencies.

Furthermore you can run:
./download_clean_up.py -h
for further information.

A log is kept for all major changes, such as removing- and moving files.

Good luck in keeping your downloads directory clean.
