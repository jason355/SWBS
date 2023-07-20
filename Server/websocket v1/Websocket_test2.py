import asyncio
import json
import websockets
import mysql.connector


connected_clients = set()


cnx = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="escko83@4L",
    database="message_database"
)
cursor = cnx.cursor()

data = []


async def handle_message(websocket, path):
    connected_clients.add(websocket)

    try:
        async for message in websocket:
            print('Received message:', message)

            # 发送消息给所有其他客户端
            for client in connected_clients:
                if client == websocket:
                    cursor.execute(f"Select * From C{message}")
                    get = cursor.fetchall()
                    for row in get:
                        record = {
                            'teacher': row[1],
                            # 'fromWhere': row[]
                            'content': row[2],
                            'sendTime': str(row[3])
                        }
                        data.append(record)
                    response = json.dumps(data, ensure_ascii=False)
                    print(response)
                    await client.send(response)
    finally:
        # 当客户端断开连接时，从已连接客户端集合中移除
        connected_clients.remove(websocket)


async def start_server():
    async with websockets.serve(handle_message, '192.168.1.110', 8000):
        print('WebSocket server started')
        await asyncio.Future()  # 持续执行服务器，直到手动停止

if __name__ == '__main__':
    asyncio.run(start_server())
