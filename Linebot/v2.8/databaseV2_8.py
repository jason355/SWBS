from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text, DateTime, update, SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func
import os

database_pass = os.getenv("dbv1p")


def getTeacher(lineId):
    session = Session()
    find_teacher = session.query(tea_infor).filter(
        tea_infor.lineID == lineId).all()
    if len(find_teacher) > 1:
        session.close()
        return "Error"
    elif len(find_teacher) == 0:
        session.close()
        return False
    else:
        session.close()
        return find_teacher[0]



def getID(name):
    session = Session()
    findID = session.query(tea_infor).filter(
        tea_infor.name == name).all()
    if len(findID) == 0:
        session.close()
        return False
    else:
        session.close()
        return findID[0]


def findTeacher(lineId):
    session = Session()
    find_teacher = session.query(tea_infor).filter(
        tea_infor.lineID == lineId).all()
    if len(find_teacher) > 1:

        session.close()
        return "Error"
    elif len(find_teacher) == 0:
            
        session.close()
        return False
    else:
        session.close()
        return True


def insertTeaInfor(lineId, map = {}):
    # try:
    if findTeacher(lineId=lineId) == False:
        session = Session()
        new_data = tea_infor(
            lineID=lineId, name=map['name'], office=map['office'], verifyStat=map['verifyStat'])
        session.add(new_data)
        session.commit()
        session.close()
    elif findTeacher(lineId=lineId) != "Error":
        session = Session()
        new_data = update(tea_infor).where(tea_infor.lineID == lineId).values(
            name=map['name'], office=map['office'], verifyStat=map['verifyStat'])
        session.execute(new_data)
        session.commit()
        session.close()

    # except:
    #     print("Someting went wrong when inserting teacher information")

# 插入資料


def insertAdmin(lineId, map={}):
    if findTeacher(lineId=lineId) == False:
        session = Session()
        new_data = tea_infor(
            lineID=lineId, name=map['name'], office=map['office'], verifyStat=map['verifyStat'], isAdmin=map['isAdmin'])
        session.add(new_data)
        session.commit()
        session.close()


def insertData(map):
    try:
        if map is None:
            return False
        session = Session()
        new_data = Data(name=map['name'], content=map['content'], office=map['office'],
                        des_grade=map['des_grade'], des_class= map['des_class'], finish_date = map['finish_date'], sound=map['sound'])
        session.add(new_data)
        session.commit()
        session.close()
        return True
        
    except Exception as e:
        session.close()
        print(e)
        return False
    

def getHistoryData(lineId):
    try:
        session = Session()
        teacher = session.query(tea_infor).filter(
            tea_infor.lineID == lineId).all()
        data = session.query(Data).filter(Data.name == teacher[0].name, Data.office == teacher[0].office).all()
        result = []
        for item in data:
            result.append(item)

        session.close()
        return result
    except Exception as e:
        session.close()

        print(e)
        return e

# 尋找管理員
def findAdmin():
    session = Session()
    find_Admin = session.query(tea_infor).filter(
        tea_infor.isAdmin == 1).all()
    data = []
    for Admin in find_Admin:
        data.append(Admin.lineID)
    if data != []:
        session.close()
        return data
    else:
        session.close()
        return False


# 判斷是否為管理員
def isAdmin(lineid):
    session = Session()
    teacher = session.query(tea_infor).filter(tea_infor.lineID == lineid).all()
    if len(teacher) > 0:
        if teacher[0].isAdmin == 1:
            session.close()
            return True
    else:
        session.close()
        return False

# 確認使用者使否認證
def verified(lineid):
    session = Session()
    check_teacher = session.query(tea_infor).filter(
        tea_infor.lineID == lineid).all()
    if check_teacher[0].verifyStat == 1:
        session.close()
        return True
    else:
        session.close()
        return False

# 修改使用者認證設定
def modifyVerifyStat(lineid):
    try:
        session = Session()
        check = session.query(tea_infor.verifyStat).filter(tea_infor.lineID == lineid)
        for item, in check:
            if item != 1:
                new = update(tea_infor).where(
                    tea_infor.lineID == lineid).values(verifyStat=1)
                session.execute(new)
                session.commit()
                session.close()
            else:
                return "Uped" # 回傳已被更新
        return True
    except Exception as e:
        session.close()

        print(e)
        return "DE" # 資料庫異常

# 取得所有未驗證帳號
def findUnVerify():
    session = Session()
    getList = session.query(tea_infor).filter(tea_infor.verifyStat == 0).all()
    if len(getList) != 0:
        session.close()
        return getList
    else:
        session.close()
        return False

# 取得所有教室lineid
def GetAllTeacherID():
    try:
        session = Session()
        teachers = [name for (name,) in session.query(tea_infor.lineID).filter(tea_infor.verifyStat == 1).all()]
        if len(teachers) != 0:
            return teachers
        else:
            return False
    except Exception as e:
        print(e)
        return False

# 刪除教師資訊
def DelTeacherData(lineid):
    try:
        session = Session()
        user_t_del = session.query(tea_infor).filter(tea_infor.lineID == lineid).first()
        session.delete(user_t_del)
        session.commit()
        session.close()

        return True
    except Exception as e:
        session.close()

        print(e)
        return False

# 刪除整個Data資料庫中資料
def DelDataAll():
    try:
        session = Session()
        rows = session.query(Data).delete()
        session.commit()
        session.close()
        return rows
        
    except Exception as e:
        session.close()
        return e

try:

    engine = create_engine(
        f"mysql+mysqlconnector://root:{database_pass}@localhost/dbv1", pool_size=50)
    Base = declarative_base()

    class tea_infor(Base):
        __tablename__ = "tea_infor"
        id = Column(Integer, primary_key=True)
        lineID = Column(String(40))
        name = Column(String(20))
        office = Column(String(20))
        isAdmin = Column(Boolean, default=False)
        verifyStat = Column(SmallInteger, default=0)

    class Data(Base):
        __tablename__ = "data"
        id = Column(Integer, primary_key=True)
        name = Column(String(40))
        content = Column(Text)
        is_new = Column(Integer, default=1)
        office = Column(String(5))
        time = Column(DateTime, default=func.now())
        finish_date = Column(String(10))
        des_grade = Column(String(3))
        des_class = Column(String(1))
        sound = Column(Integer)

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)


except SQLAlchemyError as e:
    print(f"Error: code {e} ")