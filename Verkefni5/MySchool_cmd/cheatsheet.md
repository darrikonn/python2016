# Cheatsheet for a MySchool command line
1. Get **timetable** with *-tt* or *--timetable*.

> sudo ./myschool_cmd.py -tt      

2. Get **next assignments** with *-a* or *--assignments*. You can also filter the assignments if you only want to get specific data, e.g. to only get the assignments from the Python course:

> sudo ./myschool_cmd.py -a Python

3. Get **examtable** with *-et* or *--examtable*.

> sudo ./myschool_cmd.py -et

4. Get all **new materials** with *-nm* or *--new_material*.

> sudo ./myschool_cmd.py -nm

5. Get the **book list** with *-bl* or *--booklist*.

> sudo ./myschool_cmd.py -bl

6. Get all **online quizzes** with *-q* or *--quizzes*.

> sudo ./myschool_cmd.py -q 

7. Get **all courses** for different semesters with *-c* or *--courses*. You'll need to specify the <year> and <season>, e.g. for the semester 2016 autumn. Valid seasons are: 
* winter
* spring
* summer
* autumn:

> sudo ./myschool_cmd.py -c 2016 autumn

8. Get **all groups** for different semesters with *-gr* or *--groups*. You'll need to specify the <year> and <season>, e.g. for the semester 2016 spring. Valid seasons are: 
* winter
* spring
* summer
* autumn

> sudo ./myschool_cmd.py -gr 2016 spring

9. Get **all grades** with *-g* or *--grades*. You'll need to specify one of the following as an argument:
* all
* summary
* abstract

> sudo ./myschool_cmd.py -g all

10. **Handin/Submit an assignments** with *-sa* or *--submit_assignment*. You have to specify what course this assignment belongs to and finally the name of the assignment. You can give the file with *-f* or *--file* and leave a comment with the assignment with *-m* or *--message*.

> sudo ./myschool_cmd.py -sa Python "Verkefni 5" -f myschool_cmd.zip -m "This course is granadaaaa!"
