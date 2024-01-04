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
        group_send = Column(String(1))
        finish_date = Column(String(10))

    # create session
    session = sessionmaker(bind=engine)

    # create database table
    Base.metadata.create_all(engine)
except SQLAlchemyError as e:
    print("Error setting up DAL :", e)


async def handle_message(websocket):
    # initialize the class_name variable
    class_name = None  
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


async def send_message_to_user(message, id, dest, group):

    async def send(ws, message):
        try:
            # send message
            await ws.send(message)
        except Error as e:
            print("Error sending message to user : ", e)
            # if there's error, return "u"
        break_at = 0
        while break_at < 5:
            if Cli_message[connected_clients[ws]] == id:
                return "s"
            await asyncio.sleep(1)
            break_at+=1
        return "u"

    # Traverse every data
    for ws, cls in connected_clients.items():
        # send to specified class
        if dest and not group:
            # Determine if it's the correct class
            if cls == dest:
                result = await send(ws, message)
                if result == "u":
                    # Replace not_send with the break_at loop
                    break_at = 0
                    while break_at < 4500:
                        print("failed : ", connected_clients[ws])
                        if await send(ws, message) == "s":
                            break
                        await asyncio.sleep(20)
        # send to specified grade
        elif group not in ('0', '4', '5'):
            # junior
            if group in ('7', '8', '9'):
                if cls[0] == group:
                    result = await send(ws, message)
                    if result == "u":
                        # Replace not_send with the break_at loop
                        break_at = 0
                        while break_at < 4500:
                            print("failed : ", connected_clients[ws])
                            if await send(ws, message) == "s":
                                break
                            await asyncio.sleep(20)
            # senior
            else:
                # 10th grade
                if group == '1':
                    if cls[0] == '1' and cls[1] == '0':
                        result = await send(ws, message)
                        if result == "u":
                            # Replace not_send with the break_at loop
                            break_at = 0
                            while break_at < 4500:
                                print("failed : ", connected_clients[ws])
                                if await send(ws, message) == "s":
                                    break
                                await asyncio.sleep(20)
                # 11th grade
                elif group == '2':
                    if cls[1] == '1':
                        result = await send(ws, message)
                        if result == "u":
                            # Replace not_send with the break_at loop
                            break_at = 0
                            while break_at < 4500:
                                print("failed : ", connected_clients[ws])
                                if await send(ws, message) == "s":
                                    break
                                await asyncio.sleep(20)
                # 12th grade
                elif group == '3':
                    if cls[1] == '2':
                        result = await send(ws, message)
                        if result == "u":
                            # Replace not_send with the break_at loop
                            break_at = 0
                            while break_at < 4500:
                                print("failed : ", connected_clients[ws])
                                if await send(ws, message) == "s":
                                    break
                                await asyncio.sleep(20)
        # group send
        else:
            # ALL
            if group == '0':
                result = await send(ws, message)
                if result == "u":
                    # Replace not_send with the break_at loop
                    break_at = 0
                    while break_at < 4500:
                        print("failed : ", connected_clients[ws])
                        if await send(ws, message) == "s":
                            break
                        await asyncio.sleep(20)
            # senior
            elif group == '4':
                if cls[0] not in ('7', '8', '9'):
                    result = await send(ws, message)
                    if result == "u":
                        # Replace not_send with the break_at loop
                        break_at = 0
                        while break_at < 4500:
                            print("failed : ", connected_clients[ws])
                            if await send(ws, message) == "s":
                                break
                            await asyncio.sleep(20)
            # junior
            elif group == '5':
                if cls[0] in ('7', '8', '9'):
                    result = await send(ws, message)
                    if result == "u":
                        # Replace not_send with the break_at loop
                        break_at = 0
                        while break_at < 4500:
                            print("failed : ", connected_clients[ws])
                            if await send(ws, message) == "s":
                                break
                            await asyncio.sleep(20)
    return "s"




def send_message_to_line_bot(message):
    line_bot_server_url = "https://aadc-2001-b011-14-7740-a5c8-6000-e675-e3ea.ngrok-free.app/test"  # 請替換成實際的 Line Bot Server 的 URL
    data = {"id": message}
    
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
                            dest = datas.des_grade + datas.des_class
                            if dest in connected_clients.values():
                                # send message
                                sent = await send_message_to_user(response, str(datas.id), dest, None)
                        # group send
                        elif datas.group_send:
                            # send message
                            sent = await send_message_to_user(response, str(datas.id), None, datas.group_send)
                        # check if sending successful
                        if sent == "s" :
                            try:
                            # update the data's condition and commit to database
                                db_session.query(data_access).filter_by(id=datas.id).update({"is_new": 0})
                                db_session.commit()
                                print("data sending process success")
                                send_message_to_line_bot(datas.id)
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
    await asyncio.Future()


if __name__ == '__main__':
    # start server
    asyncio.run(start_server())