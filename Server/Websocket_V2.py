import asyncio
import json
import websockets
import mysql.connector
from mysql.connector import Error
import aiomysql

# 自定義連接池參數
pool_config = {
    "host": '127.0.0.1',
    "port": 3306,
    "user": 'root',
    "password": '@@nccu1st353@csc',
    "db": 'dbv1',
    "maxsize": 100,
}


connected_clients = {}

async def handle_message(websocket, path):
    try:
        while True:
            message = await websocket.recv()
            if websocket not in connected_clients:
                connected_clients[websocket] = message
                print(f"*added new class*  class : {connected_clients[websocket]}")
    finally:
        # 當客戶端斷開連接時，從已連接客戶端集合中移除
        del connected_clients[websocket]

async def send_message_to_user(message, to_where, id):
    for websocket, cls in connected_clients.items():
        if cls == to_where:
            await websocket.send(message)
            cursor.execute(f"update data set is_new = 0 where id = {id}")
            connection.commit()           
            break



async def New_data_added():
    # 建立連接池
    pool = await aiomysql.create_pool(**pool_config)

    while True:
        async with pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT * FROM data WHERE is_new = 1")
                check = await cursor.fetchall()
                if check:
                    for datas in check:
                        response = json.dumps(datas, ensure_ascii=False)
                        await send_message_to_user(response, datas[4], datas[0])
                await cursor.execute("UPDATE data SET is_new = 0 WHERE is_new = 1")
                await connection.commit()
        await asyncio.sleep(3)

async def start_server():
    server = await websockets.serve(handle_message, '192.168.1.117', 8000)
    print('WebSocket server started')
    asyncio.create_task(New_data_added())
    await asyncio.Future()

if __name__ == '__main__':

    try:
        # 連接 MySQL/MariaDB 資料庫
        connection = mysql.connector.connect(
            host='127.0.0.1',          # 主機名稱
            database='dbv1', # 資料庫名稱
            user='root',        # 帳號
            password='@@nccu1st353@csc')  # 密碼

        if connection.is_connected():
            # 顯示資料庫版本
            db_Info = connection.get_server_info()
            print("資料庫版本：", db_Info)

            # 顯示目前使用的資料庫
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print("目前使用的資料庫：", record)

            asyncio.run(start_server())
    except Error as e:
        print("資料庫連接失敗：", e)
