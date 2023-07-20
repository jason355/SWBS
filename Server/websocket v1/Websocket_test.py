import asyncio
import websockets

connected_clients = set()


async def handle_message(websocket, path):
    connected_clients.add(websocket)

    try:
        async for message in websocket:
            print('Received message:', message)

            # 发送消息给所有其他客户端
            for client in connected_clients:
                if client != websocket:
                    await client.send(message)
    finally:
        # 当客户端断开连接时，从已连接客户端集合中移除
        connected_clients.remove(websocket)


async def start_server():
    async with websockets.serve(handle_message, '192.168.1.110', 8000):
        print('WebSocket server started')
        await asyncio.Future()  # 持续执行服务器，直到手动停止

if __name__ == '__main__':
    asyncio.run(start_server())
