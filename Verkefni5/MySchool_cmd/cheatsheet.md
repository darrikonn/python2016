# Cheatsheet for **myschool_cmd.py**
Get **timetable** with *-tt* or *--timetable*.

> sudo ./myschool_cmd.py -tt      

Get **next assignments** with *-a* or *--assignments*. You can also filter the assignments if you only want to get specific data, e.g. to only get the assignments from the Python course:

> sudo ./myschool_cmd.py -a Python

Get **examtable** with *-et* or *--examtable*.

> sudo ./myschool_cmd.py -et

Get all **new materials** with *-nm* or *--new_material*.

> sudo ./myschool_cmd.py -nm

Get the **book list** with *-bl* or *--booklist*.

> sudo ./myschool_cmd.py -bl

Get all **online quizzes** with *-q* or *--quizzes*.

> sudo ./myschool_cmd.py -q 

Get **all courses** for different semesters with *-c* or *--courses*. You'll need to specify the <year> and <season>, e.g. for the semester 2016 autumn. Valid seasons are: 
* winter
* spring
* summer
* autumn:

> sudo ./myschool_cmd.py -c 2016 autumn

Get **all groups** for different semesters with *-gr* or *--groups*. You'll need to specify the <year> and <season>, e.g. for the semester 2016 spring. Valid seasons are: 
* winter
* spring
* summer
* autumn

> sudo ./myschool_cmd.py -gr 2016 spring

Get **all grades** with *-g* or *--grades*. You'll need to specify one of the following as an argument:
* all
* summary
* abstract

> sudo ./myschool_cmd.py -g all

**Handin/Submit an assignments** with *-sa* or *--submit_assignment*. You have to specify what course this assignment belongs to and finally the name of the assignment. You can give the file with *-f* or *--file* and leave a comment with the assignment with *-m* or *--message*. You can submit multiple files, and it also checks for validation regarding file count limitations and valid extensions. <br />
I decided to not allow users to add group members from the command line, as I think the command line would not be a good choice to pick students out of 100+ possibilities. Just hand in the assignment and afterwards you can specify your group members on MySchool.

> sudo ./myschool_cmd.py -sa Python "Verkefni 5" -f myschool_cmd.zip -m "This course is granadaaaa!"
