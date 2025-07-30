import json
import logging
import uuid
from flask import request

logging.basicConfig(level=logging.DEBUG)

# 存储所有活跃连接和 session
active_connections = {}
session_store = {}

def setup_websocket_routes(app):
    @app.route('/chatws')
    def websocket_route():
        logging.info("WebSocket 路由已启用")
        if not request.environ.get('wsgi.websocket'):
            logging.error("WebSocket required")
            return "WebSocket required", 400

        ws = request.environ['wsgi.websocket']
        session_id = str(uuid.uuid4())
        logging.info(f"为客户端分配 session_id: {session_id}")

        active_connections[ws] = session_id
        session_store[session_id] = {
            'connected_at': session_id,
            'authenticated': False,
            'user': None
        }

        try:
            while True:
                message = ws.receive()
                if message is None:
                    break

                logging.info(f"收到消息: {message} (来自 session: {session_id})")

                try:
                    msg = json.loads(message)
                    command = msg.get("command")
                    data = msg.get("data", {})

                    if command == "chat":
                        user = data.get("user")
                        text = data.get("text")
                        broadcast({
                            "command": "chat",
                            "data": {
                                "user": user,
                                "text": text,
                                "timestamp": datetime.now().isoformat()
                            }
                        })

                    elif command == "stream_test":
                        user = data.get("user")
                        content = data.get("content", "这是一条测试流式消息。")
                        asyncio.run(stream_response(ws, user, content))

                    elif command == "auth":
                        user = data.get("user")
                        session_store[session_id]['authenticated'] = True
                        session_store[session_id]['user'] = user
                        ws.send(json.dumps({"status": "auth_success", "user": user}))

                    elif command == "ping":
                        ws.send(json.dumps({"command": "pong"}))

                    else:
                        ws.send(json.dumps({"status": "error", "message": "未知命令"}))

                except json.JSONDecodeError:
                    ws.send(json.dumps({"status": "error", "message": "JSON 解析失败"}))

        except Exception as e:
            logging.error(f"发生错误: {e}")
        finally:
            if ws in active_connections:
                del active_connections[ws]
            if session_id in session_store:
                del session_store[session_id]
            logging.info(f"客户端 session {session_id} 已断开")

async def stream_response(websocket, user, content):
    # 模拟流式输出：逐字发送
    for char in content:
        await asyncio.sleep(0.1)  # 模拟延迟
        await send_message(websocket, {
            "command": "stream_chunk",
            "data": {
                "user": user,
                "chunk": char
            }
        })
    await send_message(websocket, {
        "command": "stream_complete",
        "data": {
            "user": user,
            "status": "complete"
        }
    })

async def send_message(websocket, message):
    try:
        websocket.send(json.dumps(message))
    except Exception as e:
        logging.error(f"发送消息失败: {e}")

def broadcast(message):
    disconnected = []
    for conn in list(active_connections.keys()):
        try:
            conn.send(json.dumps(message))
        except:
            disconnected.append(conn)

    # 清理断开的连接
    for conn in disconnected:
        session_id = active_connections.get(conn)
        if session_id in session_store:
            del session_store[session_id]
        if conn in active_connections:
            del active_connections[conn]
