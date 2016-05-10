#!/usr/bin/env python
import argparse, requests, getpass, os, sys, traceback, prettytable
from bs4 import BeautifulSoup
#from prettytable import PrettyTable

USERNAME = 'darrik13'
PASSWORD_FILE_NAME = '.password.txt'

class Password:
    def __init__(self):
        if not self._contains_password():
            self._set_password()

    def get_password(self):
        try:
            with open(PASSWORD_FILE_NAME, 'r') as pwd:
                self._password = pwd.read()
            return self._password
        except:
            traceback.print_exc()
            sys.stderr.write('Could not get the password from {0}\n'.format(PASSWORD_FILE_NAME))

    def _set_password(self):
        try:
            with open(PASSWORD_FILE_NAME, 'w') as pwd:
                pwd.write(getpass.getpass())
            os.chown(PASSWORD_FILE_NAME, 0, -1)
            os.chmod(PASSWORD_FILE_NAME, 600)
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
            tr_soup = soup('center')[0].table.tbody('tr')[1:-1]

            # need to build my hotmail
            # table head
            table = '<table><thead>'
            for tr in tr_soup[1:3]:
                table = '{0}<tr>'.format(table)
                for th in tr.get_text().splitlines()[1:]:
                    table = '{0}<th>{1}</th>'.format(table, th)
                table = '{0}</tr>'.format(table)
            table = '{0}</thead><body>'.format(table)

            # table body
            for tr in tr_soup[3:-1]:
                table = '{0}<tr>'.format(table)
                for td in tr.get_text().splitlines()[1:]:
                    table = '{0}<th>{1}</th>'.format(table, td)
                table = '{0}</tr>'.format(table)
            table = '{0}</tbody></table>'.format(table)
            table = '<table><tbody>{0}</tbody></table>'.format(get_string_format(tr_soup))
            return prettytable.from_html(table)
        except:
            traceback.print_exc()
            sys.stderr.write('Could not get the timetable\n')

    def get_next_assignments(self):
            resp = requests.get('https://myschool.ru.is/myschool/?Page=Exe&ID=1.12',
                    auth=(USERNAME, self._pwd))
            soup = BeautifulSoup(resp.text, 'html.parser')
            tr_soup = soup('center')[0].table.tbody('tr')[:-1]
            table = '<table><tbody>{0}</tbody></table>'.format(get_string_format(tr_soup))
            return prettytable.from_html(table)

    def get_examtable(self):
            resp = requests.get('https://myschool.ru.is/myschool/?Page=Exe&ID=3.3&Tab=1',
                    auth=(USERNAME, self._pwd))
            soup = BeautifulSoup(resp.text, 'html.parser')
            tr_soup = soup('center')[0].table.tbody('tr')[:-1]
            table = '<table><tbody>{0}</tbody></table>'.format(get_string_format(tr_soup))
            return prettytable.from_html(table)

    def get_all_assignments(self):
            resp = requests.get('https://myschool.ru.is/myschool/?Page=Exe&ID=1.12',
                    auth=(USERNAME, self._pwd))
            soup = BeautifulSoup(resp.text, 'html.parser')
            tr_soup = soup('center')[1].table.tbody('tr')[:-1]
            table = '<table><tbody>{0}</tbody></table>'.format(get_string_format(tr_soup))
            return prettytable.from_html(table)

def get_string_format(s):
    return ''.join(str(x) for x in s)

def main():
    # user has to have sudo privileges because of sensitive password information
    if not os.geteuid() == 0:
        sys.stderr.write('You have to run this script with sudo privileges!\n')
        return

    parser = argparse.ArgumentParser(description='An API and a command line interface for MySchool')
    parser.add_argument('-tt', '--timetable', dest='timetable',
            help='This command will list your timetable of your courses that you\'re taking',
            action='store_true')
    parser.add_argument('-na', '--next_assignments', dest='next_assignments',
            help='This command will list your next assignments that are due in the future',
            action='store_true')
    parser.add_argument('-aa', '--all_assignments', dest='all_assignments',
            help='This command will list all your assignments that are past due date',
            action='store_true')
    parser.add_argument('-et', '--examtable', dest='examtable',
            help='This command will list all your exams in a table',
            action='store_true')

    args = parser.parse_args()

    pwd = Password()
    ms = MySchool(pwd.get_password())

    if args.timetable:
        timetable = ms.get_timetable()
        for t in timetable:
            print(t)
    elif args.examtable:
        examtable = ms.get_examtable()
        for e in examtable:
            print(e)
    elif args.next_assignments:
        assignments = ms.get_next_assignments()
        for a in assignments:
            print(a)
    elif args.all_assignments:
        assignments = ms.get_all_assignments()
        for a in assignments:
            print(a)

if __name__ == '__main__':
    sys.exit(main())
