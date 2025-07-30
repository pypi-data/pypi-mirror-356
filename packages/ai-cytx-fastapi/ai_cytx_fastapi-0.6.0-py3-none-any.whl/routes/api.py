import json
import logging
import os
from datetime import datetime

from dashscope import Application
from fastapi import APIRouter, HTTPException, File, UploadFile, Header
from fastapi.responses import StreamingResponse, JSONResponse

from config.settings import (
    dashscope_api_key,
    bailian_app_id,
    user_api_keyid,
    mcp_secret_key,
    upload_folder,
    api_base_url
)
from models.chat_model import ChatRequest, Message
from services import file_utils
from services.aliyun_service import AliyunApiService
from services.voice_translation_service import voice_translation

router = APIRouter()
logger = logging.getLogger(__name__)

logger.info("DASHSCOPE_API_KEY: %s", dashscope_api_key)
logger.info("BAILIAN_APP_ID: %s", bailian_app_id)
logger.info("USER_API_KEYID: %s", user_api_keyid)
logger.info("MCP_SECRET_KEY: %s", mcp_secret_key)
logger.info("API_BASE_URL: %s", api_base_url)

bailian_open_words = '### 开场词：\n```\n欢迎回来！我是您专属的养老顾问小瑞，很高兴再次为您服务。我注意到您之前已经填写过养老规划报 告所需的部分信息，为了更好地协助您，请问您本次是希望： 1. 调整原有报告（更新信息或修改目标） 2. 其他问题咨询 请直接告诉我您的需求，我会立刻为您安排！\n```'



"""
聊天接口
    {
	"planId": "202505151734531020000041",
	"messages": [{"role":"user","content":"项目启动时间是什么时候"}],
	"sessionId": "",
	"fileIds": [
		"file_session_bb10195356934d298c66c19639bc89c5_10509199"
		
	],
	"mode": 0
}
"""

@router.post("/chat")
async def chat(request: ChatRequest,keyId: str = Header(...),cytx_token: str = Header(...)):
    logger.debug("chat index")
    logger.info(f"Received request: {request.json()}")
    try:
        if keyId != user_api_keyid:
            raise HTTPException(status_code=401, detail="Invalid Secret Key")

        logging.info("KeyId: %s", keyId)

        if not cytx_token:
            raise HTTPException(status_code=401, detail="Invalid cytx-token")

        plan_id = request.planId
        if not plan_id:
            raise HTTPException(status_code=400, detail="Missing planId")

        mode = request.mode or 0
        messages = request.messages

        if not messages or not isinstance(messages, list) or len(messages) == 0:
            raise HTTPException(status_code=400, detail="Invalid messages")

        if messages[0].role != "system":
            messages.insert(0, Message(role="system", content=bailian_open_words))

        session_id = request.sessionId or ""

        biz_params = {
            "sk": mcp_secret_key,
            "cytxToken": cytx_token,
            "planId": plan_id
        }

        logger.info(f"biz_params: {biz_params}")
        logger.info(f"mode: {mode}")

    except Exception as e:
        logger.error(f"validate error: {e}")
        return JSONResponse(content={"code": 0, "message": f"Internal Error: {str(e)}"})

    def generate():
        try:
            if mode == 0:
                responses = Application.call(
                    api_key=dashscope_api_key,
                    app_id=bailian_app_id,
                    stream=True,
                    incremental_output=True,
                    biz_params=biz_params,
                    messages=[m.dict() for m in messages]
                )
            elif mode == 1:
                file_ids = request.fileIds
                if not file_ids or not isinstance(file_ids, list) or len(file_ids) == 0:
                    raise HTTPException(status_code=400, detail="Invalid fileIds")

                responses = Application.call(
                    api_key=dashscope_api_key,
                    app_id=bailian_app_id,
                    stream=True,
                    incremental_output=True,
                    biz_params=biz_params,
                    rag_options={"session_file_ids": file_ids},
                    messages=[m.dict() for m in messages]
                )
            else:
                raise HTTPException(status_code=400, detail="Invalid mode")

            # 标记是否为第一条消息
            first = True

            for response in responses:
                if response.status_code != 200:
                    yield json.dumps({
                        "code": 0,
                        "message": f"Error: {response.message}",
                        "request_id": response.request_id
                    })
                else:
                    chunk = {
                        "code": 1,
                        "message": "success",
                        "text": response.output.text,
                        "sessionId": response.output.session_id,
                        "planId": plan_id,
                        "request_id": response.request_id
                    }

                    # 添加 start 状态
                    if first:
                        chunk["status"] = "start"
                        first = False
                    else:
                        chunk["status"] = "processing"

                    if response.output.finish_reason == "stop":
                        chunk["status"] = "end"

                    yield json.dumps(chunk)

        except Exception as e:
            logger.error(f"Stream error: {e}")
            yield json.dumps({"code": 0, "message": f"Internal Error: {str(e)}"})

    return StreamingResponse(generate(), media_type="application/json")

"""
文件上传接口
"""
@router.post("/fileUpload")
async def file_upload(
    file: UploadFile = File(...),
    keyId: str = Header(...)
):
    """
    文件上传接口，返回 fileId。
    """

    if keyId != user_api_keyid:
        raise HTTPException(status_code=401, detail="Invalid Secret Key")

    today = datetime.now().strftime("%Y%m%d")
    date_folder = os.path.join(upload_folder, today)
    os.makedirs(date_folder, exist_ok=True)

    file_path = os.path.join(date_folder, file.filename)
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    file_size = os.path.getsize(file_path)
    file_md5 = file_utils.calculate_md5(file_path)

    file_id = AliyunApiService.do_upload_file_to_bailian(file_path, file.filename, file_md5, str(file_size))
    if not file_id:
        raise HTTPException(status_code=500, detail="File upload failed")

    return {"code": 1, "message": "success", "file_id": file_id}


@router.post("/voiceTrans")
async def voice_trans(
    file: UploadFile = File(...),
    keyId: str = Header(...)
):
    """
    语音识别专用上传接口：
    - 接收音频文件
    - 保存到服务器指定路径
    - 生成可访问的 URL
    """
    logger.info("voiceTrans")
    # 验证权限
    if keyId != user_api_keyid:
        raise HTTPException(status_code=401, detail="Invalid Secret Key")

    logger.info(f"Received audio file: {file.filename}")
    logger.info(f"Received audio file content_type: {file.content_type}")

    # 检查文件类型是否为音频文件（可选）
    allowed_types = ["audio/mpeg", "audio/mp3", "audio/x-mp3", "audio/mpg", "audio/x-mpeg", "audio/amr", "audio/AMR",
                     "audio/x-amr", "audio/wav", "audio/x-wav", "audio/wave"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Unsupported file type.")

    # 创建按天划分的子目录
    today = datetime.now().strftime("%Y%m%d")
    date_folder = os.path.join(upload_folder, today)
    os.makedirs(date_folder, exist_ok=True)

    # 文件保存路径
    file_path = os.path.join(date_folder, file.filename)

    # 保存上传的文件
    try:
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
        logger.info(f"File saved to: {file_path}")
    except Exception as e:
        logger.error(f"Error saving file: {e}")
        raise HTTPException(status_code=500, detail="File save failed.")

    # 生成访问 URL（根据你的域名或 Nginx 映射规则）
    file_url = generate_public_url("fileUploads", today, file.filename)

    # file_url = "https://ai.cytx360.com/cytxvoice/assets/hello_world_female.wav"
    
    file_text = voice_translation(file_url)
    
    if file_text is None:
        return {"code": 0, "message": "Failed to translate voice."}
    return {"code": 1, "message": "success", "text": file_text}
    
    

def generate_public_url(*parts):
    """
    根据配置生成公网访问 URL。
    假设你部署了 Nginx 映射 /voice/ 到对应目录。
    """
    base_url = api_base_url
    path = "/".join(str(p) for p in parts)
    return f"{base_url}{path}"

