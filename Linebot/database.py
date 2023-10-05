from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text, MetaData, update, SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# sql


def findTeacher(lineId):
    session = Session()
    find_teacher = session.query(tea_infor).filter(
        tea_infor.lineID == lineId).all()
    if len(find_teacher) > 1:
        return "Error"
    elif len(find_teacher) == 0:
        return False
    else:
        return find_teacher[0]


def insertTeaInfor(lineId, map={}):
<<<<<<< HEAD
    # try:
    if findTeacher(lineId=lineId) == False:
        session = Session()
        new_data = tea_infor(
            lineID=lineId, teacher=map['teacher'], fromWhere=map['fromWhere'])
        session.add(new_data)
        session.commit()
        session.close()
        session = Session()
    elif findTeacher(lineId=lineId) != "Error":
        session = Session()
        get = findTeacher(lineId)
        new_data = update(tea_infor).where(tea_infor.id == get.id).values(
            teacher=map['teacher'], fromWhere=map['fromWhere'])
        session.execute(new_data)
        session.commit()
        session.close()

    # except:
    #     print("Someting went wrong when inserting teacher information")
=======
    try:
        if findTeacher(lineId=lineId) == False:
            session = Session()
            new_data = tea_infor(
            lineID=lineId, teacher=map['teacher'], fromWhere=map['fromWhere'])
            session.add(new_data)
            session.commit()
            session.close()
            session = Session()
        elif findTeacher(lineId=lineId) != "Error":
            session = Session()
            get = findTeacher(lineId)
            new_data = update(tea_infor).where(id=get.id).values(teacher=map['teacher'], fromWhere=map['fromWhere'])
            session.execute(new_data)
            session.commit()
            session.close()

    except:
        print("Someting went wrong when inserting teacher information")
>>>>>>> 3dab0af1ab21d931bd9fdff0a9d34651695c80a9


def insertData(map={}):
    try:
        session = Session()
        new_data = Data(name=map['teacher'], content=map['content'], office=map['office'],
                        des_grade=map['des_grade'], des_class=map['des_class'])
        session.add(new_data)
        session.commit()
        session.close()
    except:
        print("Some thing went wrong when inserting Data")


try:

    engine = create_engine(
        "mysql+mysqlconnector://root:ahsnccu@localhost/dbv1", pool_size=50)
    Base = declarative_base()

    class tea_infor(Base):
        __tablename__ = "tea_infor"
        id = Column(Integer, primary_key=True)
        lineID = Column(String(40))
        teacher = Column(String(20))
        fromWhere = Column(String(20))
        isAdmin = Column(Boolean, default=False)
        verifyStat = Column(SmallInteger, default=0)

    class Data(Base):
        __tablename__ = "data"
        id = Column(Integer, primary_key=True)
        name = Column(String(15))
        content = Column(Text)
        is_new = Column(Integer, default=1)
        office = Column(String(5))
        des_grade = Column(String(3))
        des_class = Column(String(1))

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
<<<<<<< HEAD

=======

>>>>>>> 3dab0af1ab21d931bd9fdff0a9d34651695c80a9
except SQLAlchemyError as e:
    print(f"Error: code {e} ")
