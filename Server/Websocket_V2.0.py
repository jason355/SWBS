import asyncio
import json
import websockets
from mysql.connector import Error
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError




# create clients list
connected_clients = {}



try:
    # create database engine
    engine = create_engine("mysql+mysqlconnector://root:%40%40nccu1st353%40csc@localhost/dbV1", pool_size=50)

    # create model base class
    Base = declarative_base()

    # create model class
    class data_access(Base):
        __tablename__ = 'data'
        id = Column(Integer, primary_key=True)
        name = Column(String(15))
        content = Column(String(300))
        is_new = Column(Integer)
        time = Column(String(25))
        office = Column(String(5))
        des_grade = Column(String(2))
        des_class = Column(String(1))

    # create session
    session = sessionmaker(bind=engine)

    # create database table
    Base.metadata.create_all(engine)
except SQLAlchemyError as e:
    print("Error setting up DAL :", e)



async def handle_message(websocket):
    try:
        while True:
            # recive the class number which sent by client
            message = await websocket.recv()
            if websocket not in connected_clients:
                # record the class
                connected_clients[websocket] = message
                print(f"*added new class*  class : {connected_clients[websocket]}")
    except websockets.exceptions.ConnectionClosedError as e:
        # Catch server closing exception
        print("WebSocket connection closed: ", e)
    except Error as e:
        # Catch the Other Errors
        print("Error handling message :", e)
    finally:
        # when clients are disconnected, delete their record
        del connected_clients[websocket]



async def send_message_to_user(message, dest):
    # Traverse every data
    for websocket, cls in connected_clients.items():
        # Determine if it's the correct class
        if cls == dest :
            try:
                # send message
                await websocket.send(message)
                # inform message sending successful
                return "s"
            except Error as e:
                print("Error sending message to user : ", e)
            break



async def New_data_added():
    # detect new datas duplicately
    while True:
        try:
            # create database session
            db_session = session()
            try:
                # fetch datas
                check = db_session.query(data_access).filter_by(is_new=1).all()
                # Determine if there's new datas
                if check:
                    print("new data detected")  # log
                    # access every singel data
                    for datas in check:
                        # produce for-cli-data
                        record = {
                            "id": datas.id,
                            "name": datas.name,
                            "content": datas.content,
                            "is_new": datas.is_new,
                            "time": datas.time.strftime("%Y-%m-%d %H:%M:%S"),
                            "office": datas.office,
                            "des_grade": datas.des_grade,
                            "des_class": datas.des_class
                        }
                        # check if the class availible
                        dest = datas.des_grade + datas.des_class
                        if dest in connected_clients.values():
                            print("class founded")  # log
                            # produce for-cli-data
                            data = []
                            data.append(record)
                            response = json.dumps(data, ensure_ascii=False)
                            # *send message*
                            sent = await send_message_to_user(response, dest)
                            # check if sending successful
                            if sent == "s" :
                                try:
                                # update the data's condition and commit to database
                                    db_session.query(data_access).filter_by(id=datas.id).update({"is_new": 0})
                                    db_session.commit()
                                except Error as e:
                                    print("Error updating data :", e)
            except Error as e:
                print("Error fetching datas :", e)
        except Error as e:
            print("Error creating database session :", e)
        finally:
            # when the processing of a singel data is ended, close the session to avoid server's overload
            db_session.close()
            # create interval between the duplicated detection
            await asyncio.sleep(1)



async def start_server():
    # start the server
    server = await websockets.serve(handle_message, '192.168.56.1', 8000)
    print('WebSocket server started')
    # create duplicated detection
    asyncio.create_task(New_data_added())
    await asyncio.Future()



if __name__ == '__main__':
    # start server
    asyncio.run(start_server())

