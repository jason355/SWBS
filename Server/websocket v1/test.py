import asyncio
import json
import websockets
import mysql.connector
from mysql.connector import Error

try:
    # 連接 MySQL/MariaDB 資料庫
    connection = mysql.connector.connect(
        host='127.0.0.1',          # 主機名稱
        database='message_database',  # 資料庫名稱
        user='root',        # 帳號
        password='escko83@4L')  # 密碼

    if connection.is_connected():

        # 顯示資料庫版本
        db_Info = connection.get_server_info()
        print("資料庫版本：", db_Info)

        # 顯示目前使用的資料庫
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE();")
        record = cursor.fetchone()
        print("目前使用的資料庫：", record)


except Error as e:
    print("資料庫連接失敗：", e)

connected_clients = {}


async def handle_message(websocket, path):
    try:
        while True:
            message = await websocket.recv()
            if message not in processed_messages:
                connected_clients[websocket] = message
                print(
                    f"*added new class*  class : {connected_clients[websocket]}")
    finally:
        # 当客户端断开连接时，从已连接客户端集合中移除
        connected_clients.remove(websocket)


async def send_message_to_user(message, to_where):
    for websocket, cls in connected_clients.items():
        if cls == to_where:
            await websocket.send(message)
            break


async def New_data_added():
    while connected_clients != None:
        cursor.execute("SELECT * FROM data WHERE is_new = 1")
        check = cursor.fetchall()
        if check != None:
            for datas in check:
                response = json.dumps(datas, ensure_ascii=False)
                await send_message_to_user(response, datas[4])
        cursor.execute("update data set is_new = 0 where is_new = 1")


async def start_server():
    async with websockets.serve(handle_message, '192.168.1.110', 8000):
        print('WebSocket server started')
        asyncio.create_task(New_data_added())
        await asyncio.Future()  # 持续执行服务器，直到手动停止

if __name__ == '__main__':
    processed_messages = set()
    asyncio.run(start_server())
