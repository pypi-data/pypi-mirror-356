# routes/websocket.py
import json
import logging
import uuid
from datetime import datetime

from dashscope import Application
from fastapi import WebSocket
from fastapi.routing import APIRouter

from config.settings import (
    dashscope_api_key,
    bailian_app_id,
    bailian_app_id_report,
    user_api_keyid,
    mcp_secret_key,
    alibaba_cloud_workspaceid
)
from models.chat_model import ChatRequest, Message

router = APIRouter()
logger = logging.getLogger(__name__)

active_connections = {}
session_store = {}
bailian_open_words = '### 开场词：\n```\n欢迎回来！我是您专属的养老顾问小瑞，很高兴再次为您服务。我注意到您之前已经填写过养老规划报\n告所需的部分信息，为了更好地协助您，请问您本次是希望：\n1. 调整原有报告（更新信息或修改目标）\n2. 完善更多信息（补充数据）\n3. 其他问题咨询\n请直接告诉我您的需求，我会立刻为您安排！\n```'
file_system_prompt = "请必须读取所有知识库的JSON格式，将文件里的内容参数匹配到reqStr中"

@router.websocket("/chatws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    session_id = str(uuid.uuid4())
    logger.info(f"新客户端已连接，分配 session_id: {session_id}")

    active_connections[websocket] = session_id
    session_store[session_id] = {
        'connected_at': datetime.now().isoformat(),
        'authenticated': False,
        'user': None
    }

    #获取请求头
    headers = websocket.headers
    keyId = headers.get('keyId')
    logger.info("KeyId: %s", keyId)
    if keyId != user_api_keyid:
        logger.error("Invalid Secret Key")
        await websocket.send_json({"code": 0, "message": "Invalid Secret Key"})
        await websocket.close()
        return

    cytx_token = headers.get("cytx-token")
    logger.info(f"cytx_token: {cytx_token}")
    if not cytx_token:
        logger.error("Invalid cytx_token")
        await websocket.send_json({"code": 0, "message": "Invalid cytx_token"})
        await websocket.close()
        return

    logger.info(f"mcp_secret_key: {mcp_secret_key}")

    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"收到消息: {data} (来自 session: {session_id})")
            try:
                msg = json.loads(data)
                command = msg.get("command")
                payload = msg.get("data", {})

                if command == "chat" or command == "chat_report":
                    # 解析请求数据
                    chat_request = ChatRequest(**payload)
                    plan_id = chat_request.planId
                    chat_session_id = chat_request.sessionId
                    mode = chat_request.mode or 0
                    messages = chat_request.messages
                    chat_bailian_app_id = bailian_app_id
                    
                    if command == "chat_report":
                        chat_bailian_app_id = bailian_app_id_report
                    

                    if not messages or not isinstance(messages, list) or len(messages) == 0:
                        await websocket.send_json({
                            "code": 0,
                            "message": "Invalid messages",
                            "command": "error"
                        })
                        continue

                    if messages[0].role != "system" and chat_session_id is None:
                        messages.insert(0, Message(role="system", content=bailian_open_words))

                    biz_params = {
                        "user_prompt_params": {
                            "sk": mcp_secret_key,
                            "cytxToken": cytx_token,
                            "planId": plan_id}}

                    logger.info(f"biz_params: {biz_params}")

                    # 构建参数并调用 DashScope
                    if mode == 0:
                        # 如果 seeesion_id 不为空，则使用 session_id
                        if chat_session_id is not None:
                            logger.info(f"使用 chat_session_id: {chat_session_id}")
                            responses = Application.call(
                                api_key=dashscope_api_key,
                                app_id=chat_bailian_app_id,
                                stream=True,
                                incremental_output=True,
                                biz_params=biz_params,
                                session_id=chat_session_id,
                                workspace=alibaba_cloud_workspaceid,
                                #取messages中的最后一个message
                                prompt=messages[-1].content
                            )
                        else:
                            responses = Application.call(
                                api_key=dashscope_api_key,
                                app_id=chat_bailian_app_id,
                                stream=True,
                                incremental_output=True,
                                biz_params=biz_params,
                                workspace=alibaba_cloud_workspaceid,
                                messages=[m.dict() for m in messages]
                            )
                    elif mode == 1:
                        file_ids = chat_request.fileIds
                        if not file_ids or not isinstance(file_ids, list) or len(file_ids) == 0:
                            await websocket.send_json({
                                "code": 0,
                                "message": "Invalid fileIds",
                                "command": "error"
                            })
                            continue

                        # if chat_session_id is not None:
                        #     responses = Application.call(
                        #         api_key=dashscope_api_key,
                        #         app_id=bailian_app_id,
                        #         stream=True,
                        #         incremental_output=True,
                        #         biz_params=biz_params,
                        #         rag_options={"session_file_ids": file_ids},
                        #         session_id = chat_session_id,
                        #         workspace = alibaba_cloud_workspaceid,
                        #         prompt = messages[-1].content
                        #     )
                        # else:
                        #     responses = Application.call(
                        #         api_key=dashscope_api_key,
                        #         app_id=bailian_app_id,
                        #         stream=True,
                        #         incremental_output=True,
                        #         biz_params=biz_params,
                        #         rag_options={"session_file_ids": file_ids},
                        #         workspace=alibaba_cloud_workspaceid,
                        #         messages=[m.dict() for m in messages]
                        #     )
                        # change by Lazy 2025-06-08 无论有没有session_id,都不传session
                        new_messages = []
                        new_messages.insert(0, Message(role="system", content=file_system_prompt))
                        # 新建一个参数，类型是数组，第一个元素是file_system_messages，第二个元素是messages的最后一个元素
                        new_messages.insert(1, messages[-1])
                        responses = Application.call(
                                api_key=dashscope_api_key,
                                app_id=chat_bailian_app_id,
                                stream=True,
                                incremental_output=True,
                                biz_params=biz_params,
                                rag_options={"session_file_ids": file_ids},
                                workspace=alibaba_cloud_workspaceid,
                                prompt=file_system_prompt
                            )
                    else:
                        await websocket.send_json({
                            "code": 0,
                            "message": "Invalid mode",
                            "command": "error"
                        })
                        continue
                    # 标记是否为第一条消息
                    first = True

                    # 流式输出
                    for response in responses:
                        logger.info(f"返回数据: {response} (来自 session: {session_id})")
                        if response.status_code != 200:
                            await websocket.send_json({
                                "code": 0,
                                "message": f"Error: {response.message}",
                                "command": "error"
                            })
                        else:
                            session_id = response.output.session_id
                            chunk = {
                                "code": 1,
                                "message": "success",
                                "command": "stream_chunk",
                                "data": {
                                    "text": response.output.text,
                                    "sessionId": session_id,
                                    "planId": plan_id
                                }
                            }

                            # 添加 start 状态
                            if first:
                                chunk["status"] = "start"
                                first = False
                            else:
                                chunk["status"] = "processing"

                            if response.output.finish_reason == "stop":
                                chunk["status"] = "end"

                            await websocket.send_json(chunk)

                elif command == "ping":
                    await websocket.send_json({"code": 1,
                                               "message": "pong",
                                               "command": "ping"})
                else:
                    await websocket.send_json({"code": 0,
                                               "message":f"未知命令",
                                               "command": "error"})

            except json.JSONDecodeError:
                await websocket.send_json({
                                "code": 0,
                                "message": f"json解析异常",
                                "command": "error"
                            })

    except Exception as e:
        logger.error(f"发生错误: {e}")
    finally:
        logger.info(f"客户端 session {session_id} 已断开")
        if websocket in active_connections:
            del active_connections[websocket]
        if session_id in session_store:
            del session_store[session_id]

async def broadcast(message):
    disconnected = []
    for conn in list(active_connections.keys()):
        try:
            await conn.send_json(message)
        except:
            disconnected.append(conn)

    for conn in disconnected:
        session_id = active_connections.get(conn)
        if session_id in session_store:
            del session_store[session_id]
        if conn in active_connections:
            del active_connections[conn]
