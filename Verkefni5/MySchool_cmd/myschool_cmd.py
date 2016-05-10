#!/usr/bin/env python
import argparse, requests, getpass, os, sys, traceback
from bs4 import BeautifulSoup
from lxml import etree

USERNAME = 'darrik13'
PASSWORD_FILE_NAME = '.password.txt'

class Password:
    def __init__(self):
        self._password = 'fucking password (Debra Morgan)'

    def get_password(self):
        if not self._contains_password():
            self._set_password()
        return self._password

    def _set_password(self):
        try:
            with open(PASSWORD_FILE_NAME, 'w') as pwd:
                pwd.write(getpass.getpass())
            os.chown(PASSWORD_FILE_NAME, 0, -1)
            os.chmod(PASSWORD_FILE_NAME, 600)
            with open(PASSWORD_FILE_NAME, 'r') as pwd:
                self._password = pwd.read()
        except:
            traceback.print_exc()
            sys.stderr.write('Could not set the password to {0}\n'.format(PASSWORD_FILE_NAME))

    def _contains_password(self):
        return os.path.isfile(os.path.abspath(PASSWORD_FILE_NAME)) and not os.stat(PASSWORD_FILE_NAME).st_size == 0

class MySchool:
    def __init__(self, pwd):
        self._pwd = pwd

    def get_timetable(self):
        try:
            resp = requests.get('https://myschool.ru.is/myschool/?Page=Exe&ID=3.2',
                    auth=(USERNAME, self._pwd))
            soup = BeautifulSoup(resp.text, 'html.parser')
            return soup
        except:
            traceback.print_exc()
            sys.stderr.write('Could not get the timetable\n')

def main():
    # user has to have sudo privileges because of sensitive password information
    if not os.geteuid() == 0:
        sys.stderr.write('You have to run this script with sudo privileges!\n')
        return

    parser = argparse.ArgumentParser(description='An API and a command line interface for MySchool')
    parser.add_argument('-tt', '--timetable', dest='timetable',
            help='This command will list your timetable of your courses that you\'re taking',
            action='store_true')

    args = parser.parse_args()

    pwd = Password()
    ms = MySchool(pwd.get_password())
    print(ms.get_timetable())

if __name__ == '__main__':
    sys.exit(main())
