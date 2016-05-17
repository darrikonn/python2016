#!/usr/bin/env python
'''
An API and a command line interface for MySchool.
Commands can be seen in the cheatsheet on my GitHub.
In version 0.0.*, this script only runs on UNIX systems.
'''
##########################################################
__author__ = 'Darri Steinn Konradsson'
__copyright__ = 'Copyright 2016, https://github.com/darrikonn'
__credits__ = ['Darri Steinn Konradsson']
__license__ = 'GPL'
__version__ = '0.0.1'
__maintainer__ = 'Darri Steinn Konradsson'
__email__ = 'darrik13@ru.is'
##########################################################

import argparse, requests, getpass, os, sys, traceback, prettytable, re
from bs4 import BeautifulSoup


#
# public variables
#
USERNAME = 'darrik13'
PASSWORD_FILE_NAME = '.password.txt'
USE_DAY_OF_THE_WEEK = True          # used for timetable command

#
# public enum classes
#
class Season:
    Winter = 0
    Spring = 1
    Summer = 2
    Autumn = 3

class Grades:
    All = 2
    Summary = 3
    Abstract = 4

#
# custom exceptions
#
class NoCourseOrAssignment(Exception):
    pass

class FileCountExceeded(Exception):
    pass

class InvalidFileExtension(Exception):
    pass

#
# read the password from a read/write sudo protected file. If the file does not exist
# then create it with the before mentioned protection.
#
class Password:
    def __init__(self):
        self._path = os.path.join(os.path.expanduser('~'), PASSWORD_FILE_NAME)
        if not self._contains_password():
            self._set_password()

    def get_password(self):
        try:
            with open(self._path, 'r') as pwd:
                self._password = pwd.read()
            return self._password
        except:
            traceback.print_exc()
            sys.stderr.write('Could not get the password from {0}\n'.format(self._path))

    def _set_password(self):
        try:
            with open(self._path, 'w') as pwd:
                print('Please enter your Reykjavik University password')
                pwd.write(getpass.getpass())
            os.chown(self._path, 0, -1)
            os.chmod(self._path, 600)
        except:
            traceback.print_exc()
            sys.stderr.write('Could not set the password to {0}\n'.format(self._path))

    def _contains_password(self):
        return os.path.isfile(os.path.abspath(self._path)) and not os.stat(self._path).st_size == 0

class MySchool:
    def __init__(self, pwd):
        self._pwd = pwd
        self._sub = re.compile(r'<[^>]*>')

    #
    # returns a prettified table, without all inner tags
    #
    def _get_table(self, link, c_index, t_index):
        try:
            resp = requests.get(link, auth=(USERNAME, self._pwd))
            soup = BeautifulSoup(resp.text, 'html.parser')
            tr_soup = soup('center')[c_index].table.tbody('tr')[t_index:-1]
            table = '<table><thead>'
            for i, tr in enumerate(tr_soup):
                if i == 0:
                    th_temp = ''
                    for th in tr.find_all('th'):
                        if not th.a == None:
                            th_temp = '{0}<th>{1}</th>'.format(th_temp, th.a.get_text())
                        else:
                            th_temp = '{0}{1}'.format(th_temp, th)
                    table = '{0}<tr>{1}</tr></thead><tbody>'.format(table, th_temp)
                else:
                    td_temp = ''
                    for td in tr.find_all('td'):
                        if not td.a == None:
                            td_temp = '{0}<td>{1}</td>'.format(td_temp, td.a.get_text())
                        else:
                            td_temp = '{0}{1}'.format(td_temp, td)
                    table = '{0}<tr>{1}</tr>'.format(table, td_temp)
            return prettytable.from_html('{0}</tbody></table>'.format(table))
        except:
            traceback.print_exc()
            sys.stderr.write('Could not get table\n')

    #
    # find the ID of the course and the assignment in order to submit an assignment
    #
    def _get_assignment_course_ID(self, course, assignment):
        try:
            resp = requests.get('https://myschool.ru.is/myschool/?Page=Exe&ID=1.12',
                auth=(USERNAME, self._pwd))
            soup = BeautifulSoup(resp.text, 'html.parser')
            tr_soup = soup('center')[0].table.tbody('tr')[1:-1]
            href = ''
            for tr in tr_soup:
                s = tr.get_text().lower()
                if course.lower() in s and assignment.lower() in s:
                    href = tr('td')[4].a['href']
                    break
            return href
        except:
            traceback.print_exc()
            sys.stderr.write('Could not get the ID of the assignment and its course\n')

    #
    # the strip club!
    #
    def _strip_html_markup(self, s):
        return self._sub.sub('', s)

    def _get_restrictions(self, link):
        resp = requests.get(link, auth=(USERNAME, self._pwd))
        soup = BeautifulSoup(resp.text, 'html.parser')
        tr_soup = soup('center')[0].table('tr', recursive=False)
        valid_file = tr_soup[5]('td')[2].get_text().strip()
        file_count = tr_soup[6]('td')[2].get_text().strip()
        return (valid_file, file_count)

    def get_timetable(self):
        try:
            resp = requests.get('https://myschool.ru.is/myschool/?Page=Exe&ID=3.2',
                    auth=(USERNAME, self._pwd))
            soup = BeautifulSoup(resp.text, 'html.parser')
            tr_soup = soup('center')[0].table.tbody('tr')[1:-1]
            table = '<table><thead>'
            for i, tr in enumerate(tr_soup):
                if i < 2:
                    if i == 0 and USE_DAY_OF_THE_WEEK:
                        table = '{0}{1}</thead><tbody>'.format(table, tr)
                    elif i == 1 and not USE_DAY_OF_THE_WEEK:
                        table = '{0}{1}</thead><tbody>'.format(table, tr)
                else:
                    td_temp = ''
                    for td in tr.find_all('td'):
                        if not td.span == None:
                            td_temp = '{0}<td>{1}</td>'.format(td_temp,
                                    self._strip_html_markup(str(td.span.a.small).replace('<br>', '\n')))
                        else:
                            td_temp = '{0}{1}'.format(td_temp, td)
                    table = '{0}<tr>{1}</tr>'.format(table, td_temp)
            return prettytable.from_html('{0}</tbody></table>'.format(table))
        except:
            traceback.print_exc()
            sys.stderr.write('Could not get timetable\n')

    def submit_assignment(self, course, assignment, f, comment):
        try:
            data = {'athugasemdnemanda': comment}
            T = r'(?:verkID=)(\d+)(?:.*)(?:fagid=)(\d+)'
            TC = re.compile(T)
            href = self._get_assignment_course_ID(course, assignment)
            if href == '':
                raise NoCourseOrAssignment
            ids = TC.findall(href)
            link = 'https://myschool.ru.is/myschool/?Page=LMS&ID=16&fagID={0}&View=52&ViewMode=2&Tab=&Act=11&verkID={1}'.format(ids[0][1],
                    ids[0][0])
            if f == None:
                files = {'FILE': ('', '')}
                resp = requests.post(link, data=data, files=files, auth=(USERNAME, self._pwd))
            else:
                restrictions = self._get_restrictions(link)
                # check for restrictions
                if not restrictions[0] == '':
                    if not all(x[x.find('.'):] in restrictions[0] for x in f):
                        raise InvalidFileExtension(restrictions[0])
                if restrictions[1].isdigit():
                    cnt = int(restrictions[1])
                    if len(f) > cnt:
                        raise FileCountExceeded(cnt)
                files = []
                opened_files = []
                for F in f:
                    cur_f = open(os.path.abspath(F), 'rb')
                    opened_files.append(cur_f)
                    files.append((os.path.basename(F), cur_f))
                requests.post(link, data=data, files=files, auth=(USERNAME, self._pwd))
                # need to close the files afterwards
                for F in opened_files:
                    F.close()
            print('Assignment handed in!')
        except NoCourseOrAssignment:
            sys.stderr.write('No course or assignment with that name!\n')
        except FileCountExceeded as cnt:
            sys.stderr.write('File count exceeded. Maximum file count is {0}!\n'.format(cnt))
        except InvalidFileExtension as ex:
            sys.stderr.write('File extensions invalid. Valid file extensions are {0}\n'.format(ex))
        except:
            traceback.print_exc()
            sys.stderr.write('Could not submit the assignment\n')

    def get_assignments(self, filt):
        try:
            resp = requests.get('https://myschool.ru.is/myschool/?Page=Exe&ID=1.12',
                auth=(USERNAME, self._pwd))
            soup = BeautifulSoup(resp.text, 'html.parser')
            tr_soup = soup('center')[0].table.tbody('tr')[:-1]
            table = '<table><thead>{0}</thead><tbody>'.format(tr_soup[0])
            for i in range(1, len(tr_soup)):
                if filt.lower() in tr_soup[i].get_text().lower():
                    td_temp = ''
                    for td in tr_soup[i].find_all('td'):
                        if not td.a == None:
                            td_temp = '{0}<td>{1}</td>'.format(td_temp, td.a.get_text())
                        else:
                            td_temp = '{0}{1}'.format(td_temp, td)
                    table = '{0}<tr>{1}</tr>'.format(table, td_temp)
            table = '{0}</tbody></table>'.format(table)
            return prettytable.from_html(table)
        except:
            traceback.print_exc()
            sys.stderr.write('Could not get assignments\n')

    def get_courses(self, year, season):
        return self._get_table('https://myschool.ru.is/myschool/?Page=Exe&ID=7&Tab=1&Sem={0}{1}'.format(year,
                    getattr(Season, season.title())), 0, 0)

    def get_examtable(self):
        return self._get_table('https://myschool.ru.is/myschool/?Page=Exe&ID=3.3&Tab=1', 0, 0)

    def get_new_material(self):
        return self._get_table('https://myschool.ru.is/myschool/?Page=Exe&ID=1.17', 0, 0)

    def get_grades(self, command):
        return self._get_table('https://myschool.ru.is/myschool/?Page=Exe&ID=1.14',
                getattr(Grades, command.title()), 0)

    def get_online_quizzes(self):
        return self._get_table('https://myschool.ru.is/myschool/?Page=Exams&ID=13', 1, 0)

    def get_groups(self, year, season):
        return self._get_table('https://myschool.ru.is/myschool/?Page=Exe&ID=1.11&Tab=2&Sem={0}{1}'.format(year,
                getattr(Season, season.title())), 1, 0)

    #
    # this is the default behavior if no command is specified
    #
    def get_username(self):
        try:
            resp = requests.get('https://myschool.ru.is/myschool/?Page=Front',
                    auth=(USERNAME, self._pwd))
            soup = BeautifulSoup(resp.text, 'html.parser')
            return soup.div.table('tr')[3].td.div.span.get_text()
        except:
            traceback.print_exc()
            sys.stderr.write('Could not get the username\n')

    def get_book_list(self):
        try:
            resp = requests.get('https://myschool.ru.is/myschool/?Page=Exe&ID=1.13',
                    auth=(USERNAME, self._pwd))
            soup = BeautifulSoup(resp.text, 'html.parser')
            table_soup = soup('center')
            table = ''
            for t in table_soup:
                thead = '<thead>'
                tbody = '<tbody>'
                for i, tr in enumerate(t.find_all('tr')):
                    if i == 0:
                        thead = '{0}{1}'.format(thead, tr)
                    else:
                        td_temp = ''
                        for td in tr.find_all('td')[1:-1]:
                            if not td.div == None:
                                td_temp = '{0}<td>{1}</td>'.format(td_temp, td.div.get_text())
                            elif not td.p == None:
                                td_temp = '{0}<td>{1}</td>'.format(td_temp, td.p.get_text())
                            else:
                                td_temp = '{0}{1}'.format(td_temp, td)
                        tbody = '{0}<tr>{1}</tr>'.format(tbody, td_temp)
                table = '{0}<table>{1}</thead>{2}</tbody></table>'.format(table, thead, tbody)
            return prettytable.from_html(table)
        except:
            traceback.print_exc()
            sys.stderr.write('Could not get book list\n')

def print_table(table):
    for t in table:
        print(t)

#
# need to validate input files from the user
#
def validate_file(parser, filepath):
    if os.path.exists(filepath):
        return filepath
    else:
        return parser.error('The file/directory "{0}" does not exist!'.format(filepath))

def main():
    # user has to have sudo privileges because of sensitive password information
    if not os.geteuid() == 0:
        sys.stderr.write('You have to run this script with sudo privileges!\n')
        return

    parser = argparse.ArgumentParser(description='An API and a command line interface for MySchool')
    parser.add_argument('-tt', '--timetable', dest='timetable',
            help='This command will list your timetable of your courses that you\'re taking',
            action='store_true')
    parser.add_argument('-et', '--examtable', dest='examtable',
            help='This command will list all your exams',
            action='store_true')
    parser.add_argument('-nm', '--new_material', dest='new_material',
            help='This command will list all new materials',
            action='store_true')
    parser.add_argument('-bl', '--booklist', dest='booklist',
            help='This command will list all your books',
            action='store_true')
    parser.add_argument('-q', '--quizzes', dest='quizzes',
            help='This command will list all your books',
            action='store_true')
    parser.add_argument('-a', '--assignments', dest='assignments', nargs='*',
            help='This command will list your next assignments that are due in the future')
    parser.add_argument('-c', '--courses', dest='courses', nargs='*',
            help='This command will list all your course')
    parser.add_argument('-gr', '--groups', dest='groups', nargs='*',
            help='This command will list all your groups')
    parser.add_argument('-g', '--grades', dest='grades', nargs='*',
            help='This command will list all your grades')
    parser.add_argument('-sa', '--submit_assignment', dest='submit_assignment', nargs='*',
            help='This command will submit your assignment')
    parser.add_argument('-m', '--message', dest='message', metavar='STRING',
            help='A message from the student to the teacher. Follows when submitting assignment')
    parser.add_argument('-f', '--file', dest='filename', metavar='FILE',
            help='The file that is about to be submitted to MySchool',
            type=lambda f: validate_file(parser, f), nargs='+')

    args = parser.parse_args()

    # can only supply message and file if you're submitting an assignment
    if (args.filename or args.message) and args.submit_assignment == None:
        sys.stderr.write('Cannot supply "-m/--message" and "-f/--file" without "-sa/--submit_assignment"\n')
        return

    pwd = Password()
    ms = MySchool(pwd.get_password())

    if args.timetable:
        print_table(ms.get_timetable())
    elif args.examtable:
        print_table(ms.get_examtable())
    elif not args.assignments == None:
        filt = ''
        if len(args.assignments) > 0:
            filt = args.assignments[0]
        print_table(ms.get_assignments(filt))
    elif args.new_material:
        print_table(ms.get_new_material())
    elif args.quizzes:
        print_table(ms.get_online_quizzes())
    elif not args.submit_assignment == None:
        if not len(args.submit_assignment) == 2:
            sys.stderr.write('Need to specify course and assignment name!\n')
        else:
            ms.submit_assignment(args.submit_assignment[0], args.submit_assignment[1],
                    args.filename, args.message)
    elif not args.grades == None:
        if hasattr(Grades, args.grades[0].title()):
            print_table(ms.get_grades(args.grades[0]))
        else:
            sys.stderr('Command is not valid, "{0}". Valid commands are "all", "summary", "abstract"\n'.format(season))
    elif args.booklist:
        print_table(ms.get_book_list())
    elif not args.groups == None:
        if hasattr(Season, args.groups[1].title()):
            print_table(ms.get_groups(args.groups[0], args.groups[1]))
        else:
            sys.stderr('Season is not valid, "{0}". Valid seasons are "spring", "autumn", "summer", "winter"\n'.format(args.groups[1]))
    elif not args.courses == None:
        if hasattr(Season, args.courses[1].title()):
            print_table(ms.get_courses(args.courses[0], args.courses[1]))
        else:
            sys.stderr('Season is not valid, "{0}". Valid seasons are "spring", "autumn", "summer", "winter"\n'.format(args.courses[1]))
    else:
        print('Logged in as: {0}'.format(ms.get_username()))

if __name__ == '__main__':
    sys.exit(main())
