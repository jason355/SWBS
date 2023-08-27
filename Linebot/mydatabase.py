
import mysql.connector

# 建立到 MySQL 數據庫的連接
connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="escko83@4L",
    database="message",
    autocommit=True
)


def getTeacher(LineID):
    cursor = connection.cursor()
    query = f"Select teacher, fromWhere from tea_infor WHERE lineID = '{LineID}'"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    for row in result:
        if row != None:
            print(row)
            # connection.close()
            return row[0], row[1]


def insertIdNam(LineID, teacherName):
    cursor = connection.cursor()
    query = f"Insert into tea_infor(lineID, teacher, fromWhere) values('{LineID}', '{teacherName}', 'null');"
    cursor.execute(query)
    cursor.close()
    # connection.close()


def insertFromWhere(LineID, fromWhere):
    cursor = connection.cursor()
    query = f"UPDATE tea_infor Set fromWhere = '{fromWhere}' where lineID = '{LineID}';"
    cursor.execute(query)
    cursor.close()


# insertIdNam("Jason", "林珈生")
# insertFromWhere("Jason", "教務處")
print(getTeacher("Jason"))


def insertMessage(teacher, fromWhere, content, toWho, isNew, sendtime):
    cursor = connection.cursor()
    query = f"Insert into data (teacher, fromWhere, content, sendtime, toWho, isNew) values('{teacher}', '{fromWhere}', '{content}', '{sendtime}', '{toWho}', '{isNew}');"
    cursor.execute(query)
    cursor.close()


def updateMessage(content, toWho):
    cursor = connection.cursor()
    query = f"UPDATE data Set toWho = '{toWho}' where content = '{content}';"
    cursor.execute(query)
    cursor.close()


def getMessage():
    cursor = connection.cursor()
    query = f"Select * from message;"
    cursor.execute(query)
    cursor.fetchall(query)
    result = cursor
    return list(result)
