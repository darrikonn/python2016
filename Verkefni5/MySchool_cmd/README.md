# MySchool command line
This is a Python3 MySchool command line application.<br />
* The *requirements/dependencies* can be seen in **requirements.txt**.<br />
* An informal *cheatsheet* can be seen in **cheatsheet.md**.<br />

## Setup
Install the requirements with:

> sudo pip install -r requirements.txt

Next open *myschool_cmd.py* and change the global **USERNAME** in *line 24* to your own username.<br />
You need to run the script with sudo privilege, where in your first run you will be prompt for a password from MySchool. This password will be saved to *.password.txt*, located in your */root* directory, and only root will be able to both read and write. <br/>
Optionally you can change all three global variables, inside the script:
* USERNAME
* PASSWORD_FILE_NAME
* USE_DAY_OF_WEEK

## Run
After the setup, you can run the commands that are listed in the *cheatsheet*, e.g.:

> sudo ./myschool_cmd.py -tt

This command will list your timetable.<br />

## Recommended options (not mandatory)
I recommend first either moving the file or creating a symbolic link from *myschool_cmd.py* to */usr/bin*, with:

> sudo ln -s /full/path/to/myschool_cmd.py /usr/bin/myschool_cmd.

After that create an alias so it will be easier to run the script.
##### For bash users:
Open ~/.bashrc (or ~/.bash_profile if you are using Mac OS X) and append this to the end of the file:

> alias ms="sudo myschool_cmd.py"

##### For zsh users:
Open ~/.zshrc and append this to the end of the file:

> alias ms="sudo ./myschool_cmd.py"

Now you should be able to run the script, simply by running:

> ms -tt
