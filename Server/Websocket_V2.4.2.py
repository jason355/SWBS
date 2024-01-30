import asyncio
import json
import websockets
import requests
from mysql.connector import Error
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError


# Please set up your internet information here
ip = "192.168.56.1"
port = 8000
#Please set up your internet information here

# create var to store the client's reply
Cli_message = {}

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
        finish_date = Column(String(10))

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
            msg = await websocket.recv()
            print("Recieved : ", msg)
            if websocket not in connected_clients:
                # record the class
                connected_clients[websocket] = msg
                # update the class_name
                class_name = msg
                print(f"*added new class*  class : {connected_clients[websocket]}")
            Cli_message[connected_clients[websocket]] = msg
            print(Cli_message)
    except websockets.exceptions.ConnectionClosedError as e:
        # Catch server closing exception
        print("WebSocket connection closed: ", e)
    except websockets.exceptions.ConnectionClosedOK as e :
        print(f"WebSocket connection closed OK, class = {class_name}; ", e)
    except Error as e:
        # Catch the Other Errors
        print("Error handling message :", e)
    finally:
        # when clients are disconnected, delete their record
        if websocket in connected_clients:
            del connected_clients[websocket]


async def send_message_to_user(message, id, dest):

    async def send(ws, message):
        try:
            # send message
            await ws.send(message)
        except Error as e:
            print("Error sending message to user : ", e)
        break_at = 0
        while break_at < 5:
            if Cli_message[connected_clients[ws]] == id:
                return "s"
            await asyncio.sleep(1)
            break_at+=1
        # if there's error, return "u"
        return "u"

    # Traverse every data
    for ws, cls in connected_clients.items():
        # send to specified class
        if dest :
            # Determine if it's the correct class
            if cls == dest:
                return await send(ws, message)




def send_message_to_line_bot(time, name, cls, content):
    line_bot_server_url = "http://192.168.56.1:8080/test"  # 請替換成實際的 Line Bot Server 的 URL
    data = {"time": time, "name": name, "cls": cls, "content": content}
    
    response = requests.post(line_bot_server_url, json=data)
    
    if response.status_code == 200:
        print("Message sent successfully to Line Bot Server")
    else:
        print("Failed to send message to Line Bot Server. Status code:", response.status_code)




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
                    # access every singel data
                    for datas in check:
                        # produce for-cli-data
                        record = {
                            "id": datas.id,
                            "name": datas.name,
                            "class": datas.des_grade + datas.des_class,
                            "content": datas.content,
                            "is_new": datas.is_new,
                            "time": datas.time.strftime("%Y-%m-%d %H:%M:%S"),
                            "office": datas.office,
                            "finish_date": datas.finish_date
                        }
                        # produce for-cli-data
                        data = []
                        data.append(record)
                        response = json.dumps(data, ensure_ascii=False)
                        # declare check var
                        sent = None
                        # sent to a specified class
                        if datas.des_class and datas.des_grade:
                            # check if the class availible
                            if datas.des_grade[1] == "7" or datas.des_grade[1] == "8" or datas.des_grade[1] == "9":
                                dest = datas.des_grade[1]+datas.des_grade[0]+datas.des_class
                            else:
                                dest = datas.des_grade + datas.des_class
                            if dest in connected_clients.values():
                                # send message
                                sent = await send_message_to_user(response, str(datas.id), dest)
                        # check if sending unsuccessful
                        if sent == "u" :
                            print("data sending time exceeded, ID = ", datas.id)
                            try:
                                send_message_to_line_bot(datas.time.strftime("%Y-%m-%d %H:%M:%S"), datas.name, dest, datas.content)
                            except Error as e:
                                print("Error Sending message to linebot :", e)
                        if sent :
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
    server = await websockets.serve(handle_message, ip, port)
    print('WebSocket server started')
    # create duplicated detection
    asyncio.create_task(New_data_added())
    await server.wait_closed()


if __name__ == '__main__':
    # start server
    asyncio.run(start_server())
