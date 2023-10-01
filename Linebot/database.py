from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError


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
        "mysql+mysqlconnector://root:escko83%404L@localhost/message", pool_size=50)
    Base = declarative_base()

    class Teacher(Base):
        __tablename__ = "teacher"
        id = Column(Integer, primary_key=True)
        lineID = Column(String(40))
        teacher = Column(String(20))
        fromWhere = Column(String(20))

    class Data(Base):
        __tablename__ = "data"
        id = Column(Integer, primary_key=True)
        name = Column(String(15))
        content = Column(String)
        is_new = Column(Integer)
        office = Column(String(5))
        des_grade = Column(String(3))
        des_class = Column(String(1))

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

except SQLAlchemyError as e:
    print(f"Error: code {e} ")
