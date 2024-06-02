import asyncio
import websockets
import subprocess
import json
import datetime

async def check_server(uri):
    ping_message = "hello server"
    try:
        async with websockets.connect(uri) as websocket:
            ping = {
                "header": "M1",
                "ping": ping_message
            }
            ping = json.dumps(ping, ensure_ascii=False)
            await websocket.send(ping)
            response = await websocket.recv()
            response = json.loads(response)  # 解析接收到的消息
            if response.get("ping") == ping_message:
                return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def restart_server(command):
    try:
        print("Restarting server...")
        # 使用 `start` 命令在新的命令行窗口中运行命令
        subprocess.Popen(f'start cmd /c {command}', shell=True)
        print("Server restart command issued successfully\n", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    except subprocess.CalledProcessError as e:
        print(f"Failed to restart server: {e}")

async def monitor_server(uri, check_interval, restart_command):
    while True:
        server_running = await check_server(uri)
        if not server_running:
            restart_server(restart_command)
        await asyncio.sleep(check_interval)

if __name__ == "__main__":
    # WebSocket服务器的URI
    websocket_uri = "ws://140.119.99.17:80"

    # 检查间隔时间（秒）
    check_interval = 1

    # 重启服务器的命令（根据你的服务器配置进行修改）
    restart_command = r'python "C:\CSBS\run\Websocket_V2.5.py"'

    # 开始监控
    asyncio.get_event_loop().run_until_complete(monitor_server(websocket_uri, check_interval, restart_command))
