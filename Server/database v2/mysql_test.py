import mysql.connector
import datetime


def nextgrade(Class):
    if Class == 107:
        Class = 111
    if Class == 117:
        Class = 121


def create_high_school_tables(Class):
    while Class != 127:
        create_table = f"Create table C{Class} (id serial PRIMARY KEY, teacher varchar(40), content TEXT, sendTime DATETIME);"
        cursor.execute(create_table)
        cnx.commit()
        Class += 1
        nextgrade(Class)


def drop_high_school_table(Class):
    while Class != 127:
        drop_table = f"drop table C{Class}"
        cursor.execute(drop_table)
        cnx.commit()
        Class += 1
        nextgrade(Class)


def show_all_tables():
    query = "SHOW TABLES"
    cursor.execute(query)
    results = cursor.fetchall()
    for row in results:
        print(row)


        
cnx = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="escko83@4L",
    database="message"
)

cursor = cnx.cursor()
Class = 101

# create_high_school_tables(Class)
now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(now_time)

# while Class != 127:
#     print(f"IN {Class} ")
#     insert_values = f"Insert into C{Class} (teacher, content, sendtime) values ('中之敏', '咖啡好難喝，這到底是誰發明的東西，該死', '{now_time}');"
#     cursor.execute(insert_values)
#     cnx.commit()
#     insert_values = f"Insert into C{Class} (teacher, content, sendtime) values ('蔡小姐', '沒什麼好說的', '{now_time}');"
#     cursor.execute(insert_values)
#     cnx.commit()
#     Class += 1
#     nextgrade(Class)


Class = 101
while Class != 127:
    cursor.execute(f"Select * from C{Class};")
    get = cursor.fetchall()
    print(get)
    Class += 1
    nextgrade(Class)

# cursor.execute("Delete from C101")


cnx.close()
