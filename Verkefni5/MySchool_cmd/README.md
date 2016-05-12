# MySchool command line
This is a Python3 MySchool command line application.<br />
* The *requirements/dependencies* can be seen in **requirements.txt**.<br />
* An informal *cheatsheet* can be seen in **cheatsheet.md**.<br />

## Setup
In order to run this script, you should open *myschool_cmd.py* and change the global **USERNAME** in *line 8* to your own username..<br />
You need to run the script with sudo privilege, where in your first run you will be prompt for a password from MySchool. This password will be saved to *.password.txt*, located in your *$HOME* directory, and only root will be able to both read and write. 

## Run
After the setup, you can run the commands that are listed in the *cheatsheet*, e.g.:

> sudo ./myschool_cmd.py -tt

This command will list your timetable.<br />

## Recommended options (not mandatory)
I recommend first either moving the file or creating a symbolic link from *myschool_cmd.py* to */bin*, with:

> sudo ln -s /full/path/to/myschool_cmd.py /bin/myschool_cmd.

After that create an alias so it will be easier to run the script.
##### For bash users:
Open ~/.bashrc and append this to the end of the file:

> alias ms="sudo myschool_cmd.py"

##### For zsh users:
Open ~/.zshrc and append this to the end of the file:

> alias ms="sudo ./myschool_cmd.py"

Now you should be able to run the script, simply by running:

> ms -tt
