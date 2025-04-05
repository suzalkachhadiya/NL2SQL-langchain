import sqlite3

# connect to sqlite
connection=sqlite3.connect("student.db")

## create a cursor objrct to insert recor, createtable
cursor=connection.cursor()

# create table
table_info="""
    create table IF NOT EXISTS STUDENT(NAME VARCHAR(25), CLASS VARCHAR(25),SECTION VARCHAR(25),MARKS INT)
"""

cursor.execute(table_info)

##  insert some more records
cursor.execute("""INSERT INTO STUDENT values('Suzal','Data science','A','90')""")
cursor.execute("""INSERT INTO STUDENT values('Krish','Data science','B','100')""")
cursor.execute("""INSERT INTO STUDENT values('Tapan','Data science','A','88')""")
cursor.execute("""INSERT INTO STUDENT values('Kenil','Web Develpment','A','70')""")
cursor.execute("""INSERT INTO STUDENT values('Satyam','Web Develpment','A','67')""")

# Display all the recorDs
print("the inserteD records are")
data=cursor.execute("""SELECT * FROM STUDENT""")

for row in data:
    print(row)

connection.commit()
connection.close()