#!/usr/bin/env python
import argparse, requests, getpass, os, sys, traceback, prettytable, re
from bs4 import BeautifulSoup
# tabulate

#
# public variables
#
USERNAME = 'darrik13'
PASSWORD_FILE_NAME = '.password.txt'

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

    def _get_table(self, link, c_index, t_index):
        try:
            resp = requests.get(link,
                    auth=(USERNAME, self._pwd))
            soup = BeautifulSoup(resp.text, 'html.parser')
            tr_soup = soup('center')[c_index].table.tbody('tr')[t_index:-1]
            table = '<table><tbody>{0}</tbody></table>'.format(get_string_format(tr_soup))
            return prettytable.from_html(table)
        except:
            traceback.print_exc()
            sys.stderr.write('Could not get table\n')

    def _get_assignment_course_ID(self, course, assignment):
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

    def get_timetable(self):
        return self._get_table('https://myschool.ru.is/myschool/?Page=Exe&ID=3.2', 0, 1)

    def submit_assignment(self, course, assignment, f, comment):
        data = {'athugasemdnemanda': comment, 'FILE': f}
        try:
            T = r'(?:verkID=)(\d+)(?:.*)(?:fagid=)(\d+)'
            TC = re.compile(T)
            href = self._get_assignment_course_ID(course, assignment)
            if href == '':
                raise NoCourseOrAssignment
            ids = TC.findall(href)
            link = 'https://myschool.ru.is/myschool/?Page=LMS&ID=16&fagID={0}&View=52&ViewMode=2&Tab=&Act=11&verkID={1}'.format(ids[0][1],
                    ids[0][0])
            resp = requests.post(link, data=data, auth=(USERNAME, self._pwd))
        except NoCourseOrAssignment:
            sys.stderr.write('No course or assignment with that name!\n')
        except:
            traceback.print_exc()
            sys.stderr.write('Could not submit the assignment')

    def get_assignments(self, filt):
        resp = requests.get('https://myschool.ru.is/myschool/?Page=Exe&ID=1.12',
            auth=(USERNAME, self._pwd))
        soup = BeautifulSoup(resp.text, 'html.parser')
        tr_soup = soup('center')[0].table.tbody('tr')[:-1]
        table = '<table><thead>{0}</thead><tbody>'.format(tr_soup[0])
        for i in range(1, len(tr_soup)):
            if filt.lower() in tr_soup[i].get_text().lower():
                table = '{0}{1}'.format(table, tr_soup[i])
        table = '{0}</tbody></table>'.format(table)
        return prettytable.from_html(table)

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

    def get_username(self):
        resp = requests.get('https://myschool.ru.is/myschool/?Page=Front',
                auth=(USERNAME, self._pwd))
        soup = BeautifulSoup(resp.text, 'html.parser')
        return soup.div.table('tr')[3].td.div.span.get_text()

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
                        tbody = '{0}<tr>{1}</tr>'.format(tbody,
                                get_string_format(tr.find_all('td')[1:-1]))
                table = '{0}<table>{1}</thead>{2}</tbody></table>'.format(table, thead, tbody)
            return prettytable.from_html(table)
        except:
            traceback.print_exc()
            sys.stderr.write('Could not get new material\n')

def get_string_format(s):
    return ''.join(str(x) for x in s)

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
            type=lambda f: validate_file(parser, f))

    args = parser.parse_args()

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
            print('Assignment handed in!')
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
