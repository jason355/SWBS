import asyncio
import json
import os
import websockets
import requests
from mysql.connector import Error
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError


# Please set up your internet information here
ip = "140.119.99.17"
port = 80
# Please set up your internet information here

# create var to store the client's reply
Cli_message = {}

# create clients list
connected_clients = {}


try:
    # access enviroment variable to get db password
    database_pass = os.getenv("dbv1p")
    # create database engine
    engine = create_engine(f"mysql+mysqlconnector://root:{database_pass}@localhost/dbV1", pool_size=50)


    # create model base class
    Base = declarative_base()

    # create model class
    class data_access(Base):
        __tablename__ = 'data'
        id = Column(Integer, primary_key=True)
        name = Column(String(15))
        lineID = Column(String(45))
        hash = Column(String(40))
        content = Column(String(300))
        is_new = Column(Integer)
        time = Column(String(25))
        office = Column(String(5))
        des_grade = Column(String(2))
        des_class = Column(String(1))
        finish_date = Column(String(10))
        sound = Column(Integer)

    # create session
    session = sessionmaker(bind=engine)

    # create database table
    Base.metadata.create_all(engine)
except SQLAlchemyError as e:
    print("Error setting up DAL :", e)


async def handle_message(websocket):
    # create a message list of every client's message
    msg = {}
    while True:
        # recive the class number which sent by client
        try:
            msg[websocket] = await asyncio.wait_for(websocket.recv(), timeout=5.0)  # Set the expired time to 5s
            print("Recieved : ", msg[websocket])
        except asyncio.TimeoutError:
            continue
        except websockets.exceptions.ConnectionClosedError as e:
            print("WebSocket connection closed: ", e)
            await websocket.close()
            break
        except websockets.exceptions.ConnectionClosedOK as e:
            print(f"WebSocket connection closed OK, class = {connected_clients[websocket]}; ", e)
            await websocket.close()
            break
        except Exception as e:
            print(f"Other error: {e}")
            await websocket.close()
            break
        # if the message was sent by a new client
        if websocket not in connected_clients:
            # record the message it sent as a class name
            connected_clients[websocket] = msg[websocket]
            print(f"*added new class*  class : {connected_clients[websocket]}")
        # anyhow, record the message into msg list
        Cli_message[connected_clients[websocket]] = msg[websocket]
    # while disconnected, delete the data of the client
    if websocket in connected_clients:
        del connected_clients[websocket]


async def send_message_to_user(message, id, dest):
    # define the funciton of sending process
    async def send(ws, message):
        try:
            # send message
            await ws.send(message)
        except Error as e:
            print("Error sending message to user : ", e)
        break_at = 0
        # waiting 60s for the client's return value to finish the sending process
        while break_at < 600:
            if ws in connected_clients:
                # detect if the message of the client in the msg list has updated to the return value
                if Cli_message[connected_clients[ws]] == id:
                    print("data sending success, id : ", id)
                    # if client did return the value, return "u"
                    return "s"
            await asyncio.sleep(0.1)
            break_at += 1
        # if client didn't return the value, return "u"
        return "u"
    # Traverse every data
    for ws, cls in connected_clients.items():
        # if it's the correct class, start sending process
        if cls == dest:
            return await send(ws, message)


def send_message_to_line_bot(time, name, cls, content):
    # setting the information of http sending
    line_bot_server_url = "https://d8b6-140-119-99-80.ngrok-free.app/return"
    data = {"time": time, "name": name, "cls": cls, "content": content}
    try:
        # post the data on the url
        response = requests.post(line_bot_server_url, json=data)
        response.raise_for_status()
        print("Message sent successfully to Line Bot Server")
    except requests.exceptions.RequestException as e:
        print("Failed to send message to Line Bot Server. Error:", e)


async def New_data_added():
    # detect new datas duplicately
    while True:
        try:
            # create database session
            db_session = session()
            try:
                # fetch datas
                check = db_session.query(data_access).filter_by(is_new=1).all()
                # if there are new datas
                if check:
                    # access every single data
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
                            "finish_date": datas.finish_date,
                            "sound": datas.sound
                        }
                        # produce for-cli-data
                        data = []
                        data.append(record)
                        response = json.dumps(data, ensure_ascii=False)
                        # declare check variable
                        sent = None
                        # modify the format of sending destination
                        if datas.des_grade[1] == "7" or datas.des_grade[1] == "8" or datas.des_grade[1] == "9":
                            dest = datas.des_grade[1] + datas.des_grade[0] + datas.des_class
                        else:
                            dest = datas.des_grade + datas.des_class
                        # check if the class in the clients list
                        if dest in connected_clients.values():
                            # send message
                            sent = await send_message_to_user(response, str(datas.id), dest)
                        # check if sending unsuccessful
                        if sent == "u":
                            print("data sending time exceeded, ID = ", datas.id)
                            # send message to linebot to inform the teacher the sending was failed
                            try:
                                send_message_to_line_bot(datas.time.strftime("%Y-%m-%d %H:%M:%S"), datas.name, dest, datas.content)
                            except Error as e:
                                print("Error Sending message to linebot :", e)
                        # anyhow, set the status of the message to old message
                        if sent:
                            try:
                                # update the data's status and commit to database
                                db_session.query(data_access).filter_by(id=datas.id).update({"is_new": 0})
                                db_session.commit()
                            except Error as e:
                                print("Error updating data :", e)
            except Error as e:
                print("Error fetching datas :", e)
        except Error as e:
            print("Error creating database session :", e)
        finally:
            # when the processing of a single data is ended, close the session to avoid server's overload
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
