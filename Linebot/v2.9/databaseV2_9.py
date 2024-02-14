from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text, DateTime, update, SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func
import os
import hashlib


# 取得資料庫密碼
database_pass = os.getenv("dbv1p")


# 取得教師資訊
def getTeacher(lineId):
    try:
        with Session() as session:
            teacher = session.query(tea_infor).filter(tea_infor.lineID == lineId).one_or_none()
            
            if teacher:
                return teacher
            return False
    except Exception as e:
        raise e

# 確認是否有此教師
def findTeacher(lineId):
    try:
        with Session() as session:
            find_teacher = session.query(tea_infor).filter(
                tea_infor.lineID == lineId).one_or_none()
            if find_teacher:
                return True
            else:
                return False
    except Exception as e:
        raise e

# 使用教師名稱取得教師資訊
def getID(name):
    try: 
        with Session() as session:
            findID = session.query(tea_infor).filter(
                tea_infor.name == name).one_or_none()
            if findID:
                return findID
            else:
                return False
    except Exception as e:   
        raise e
    



# 插入教師資訊
def insertTeaInfor(lineId, map = {}):
    try:
        with Session() as session:
            if not findTeacher(lineId):
                session = Session()
                new_data = tea_infor(
                    lineID=lineId, name=map['name'], office=map['office'], verifyStat=map['verifyStat'])
                session.add(new_data)
                session.commit()
                
                return True
            else:
                session = Session()
                new_data = update(tea_infor).where(tea_infor.lineID == lineId).values(
                    name=map['name'], office=map['office'], verifyStat=map['verifyStat'])
                session.execute(new_data)
                session.commit()
                
                return True

    except Exception as e:
        print(e)
        return False 




# 插入首位管理員
def insertAdmin(lineId, map={}):
    try:
        with Session() as session:
            if not findTeacher(lineId):
                new_data = tea_infor(
                    lineID=lineId, name=map['name'], office=map['office'], verifyStat=map['verifyStat'], isAdmin=map['isAdmin'])
                session.add(new_data)
                session.commit()
                return True
            else:
                new = update(tea_infor).where(
                            tea_infor.lineID == lineId).values(isAdmin=1)
                session.execute(new)
                session.commit()
                return True
    except Exception as e:
        raise e

# 插入廣播訊息
def insertData(map):
    try:
        with Session() as session:
            if map is None:
                return False

            new_data = Data(name=map['name'], lineID=map['lineID'], hash=map['hash'],content=map['content'], office=map['office'], time=map['time'],
                            des_grade=map['des_grade'], des_class= map['des_class'], finish_date = map['finish_date'], sound=map['sound'])
            session.add(new_data)
            session.commit()
            return True
    except Exception as e:
        raise e
        

def getHistoryData(lineId):
    try:
        with Session() as session:
            data = session.query(Data).filter(Data.lineID == lineId).all()
            result = []
            for item in data:
                result.append(item)
            return result
    except Exception as e:
        raise e

# 尋找管理員
def findAdmin():
    try:
        with Session() as session:
            find_Admin = session.query(tea_infor).filter(
                tea_infor.isAdmin == 1).all()
            data = []
            for Admin in find_Admin:
                data.append(Admin.lineID)
            if data != []:
                return data
            else:
                return False
    except Exception as e:
        raise e


# 判斷是否為管理員
def isAdmin(lineId):
    try:
        with Session() as session:
            admin = session.query(tea_infor.isAdmin).filter(tea_infor.lineID == lineId).one_or_none()
            return admin
    except Exception as e:
        raise e
    

# 確認使用者使否認證
def verified(lineId):
    try:
        with Session() as session:
            check_teacher = session.query(tea_infor.verifyStat).filter(
                tea_infor.lineID == lineId).one_or_none()
            if check_teacher:
                return True
            else:
                return False
    except Exception as e:
        raise e

# 修改使用者認證設定
def modifyVerifyStat(lineId):
    try:
        with Session() as session:
            user = session.query(tea_infor).filter(tea_infor.lineID == lineId).one_or_none()
            if user:
                if not user.verifyStat:
                    new = update(tea_infor).where(
                        tea_infor.lineID == lineId).values(verifyStat=1)
                    session.execute(new)
                    session.commit()
                    return True
                else:
                    return "Uped"
            else:
                return False
    except Exception as e:
        raise e

# 取得所有未驗證帳號
def findUnVerify():
    try:
        with Session() as session:
            getList = session.query(tea_infor).filter(tea_infor.verifyStat == 0).all()
            if len(getList) != 0:
                return getList
            else:
                return False
    except Exception as e:
        raise e

# 取得所有教室lineId
def GetAllTeacherID():
    try:
        with Session() as session:
            teachers = [name for (name,) in session.query(tea_infor.lineID).filter(tea_infor.verifyStat == 1).all()]
            if len(teachers) != 0:
                return teachers
            else:
                return False
    except Exception as e:
        print(e)
        return False

# 刪除教師資訊
def DelTeacherData(lineId):
    try:
        with Session() as session:
            user_t_del = session.query(tea_infor).filter(tea_infor.lineID == lineId).one_or_none()
            if user_t_del:
                session.delete(user_t_del)
                session.commit()
                return True
            else:
                return False
    except Exception as e:
        raise e

# 刪除整個Data資料庫中資料
def DelDataAll():
    try:
        with Session() as session:
            rows = session.query(Data).delete()
            session.commit()
            return rows
    except Exception as e:
        return False
    


try:

    engine = create_engine(
        f"mysql+mysqlconnector://root:{database_pass}@localhost/dbv1", pool_size=50)
    Base = declarative_base()

    class tea_infor(Base):
        __tablename__ = "tea_infor"
        id = Column(Integer, primary_key=True)
        lineID = Column(String(45))
        name = Column(String(20))
        office = Column(String(20))
        isAdmin = Column(Boolean, default=False)
        verifyStat = Column(SmallInteger, default=0)

    class Data(Base):
        __tablename__ = "data"
        id = Column(Integer, primary_key=True)
        name = Column(String(40))
        lineID = Column(String(45))
        hash = Column(String(40))
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