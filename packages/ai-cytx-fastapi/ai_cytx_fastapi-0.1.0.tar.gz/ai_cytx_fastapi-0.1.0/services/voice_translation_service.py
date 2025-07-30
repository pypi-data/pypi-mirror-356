import logging

import dashscope
import requests

from config.settings import dashscope_api_key

logger = logging.getLogger(__name__)

def voice_translation(file_url:str) -> str:
    dashscope.api_key = dashscope_api_key
    
    task_response = dashscope.audio.asr.Transcription.async_call(
        model='paraformer-v1',
        file_urls=[file_url]
    )
    transcribe_response = dashscope.audio.asr.Transcription.wait(task=task_response.output.task_id)
    # print("transcribe_response:%s", transcribe_response.output)
    logger.info("transcribe_response:%s", transcribe_response.output)
    
    """
        {"task_id": "de7c356e-bad1-4b8a-b073-ff963dd2b69c", "task_status": "SUCCEEDED", "submit_time": "2025-06-17 15:05:00.664", "scheduled_time": "2025-06-17 15:05:00.696", "end_time": "2025-06-17 15:05:01.208", "results": [{"file_url": "https://ai.cytx360.com/cytxvoice/assets/hello_world_female.wav", "transcription_url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/paraformer-v2/20250617/15%3A05/389b2113-a29e-46fc-9b5e-1d5af1a10b8a-1.json?Expires=1750230301&OSSAccessKeyId=LTAI5tQZd8AEcZX6KZV4G8qL&Signature=8yP0nNAG2IGjOM%2B04C2UKjOGqSc%3D", "subtask_status": "SUCCEEDED"}], "task_metrics": {"TOTAL": 1, "SUCCEEDED": 1, "FAILED": 0}}
    """
    return_str = get_transcribed_text(transcribe_response.output)
    if return_str:
        # print("transcribe_response:%s", return_str)
        logger.info("transcribe_response:%s", return_str)
    return return_str


def get_transcribed_text(task_response: dict) -> str | None:
    """
    根据 dashscope 的语音识别任务响应结果，获取最终的 transcribed text。

    :param task_response: dashscope 返回的任务结果字典
    :return: 提取到的文本内容，失败则返回 None
    """
    if not isinstance(task_response, dict):
        # print("Invalid task response format.")
        logger.error("Invalid task response format.")
        return None

    task_status = task_response.get("task_status")
    if task_status != "SUCCEEDED":
        # print(f"Task not succeeded. Status: {task_status}")
        logger.error(f"Task not succeeded. Status: {task_status}")
        return None

    results = task_response.get("results", [])
    if not results or not isinstance(results, list):
        # print("No results found in the task response.")
        logger.error("No results found in the task response.")
        return None

    # 取第一个结果（通常只有一个）
    result = results[0]
    transcription_url = result.get("transcription_url")

    if not transcription_url:
        # print("No transcription_url found in the result.")
        logger.error("No transcription_url found in the result.")
        return None

    try:
        # 下载 transcription_url 的 JSON 内容
        response = requests.get(transcription_url)
        response.raise_for_status()  # 确保请求成功

        transcription_data = response.json()

        # 获取 transcripts.text 字段
        transcripts = transcription_data.get("transcripts", [])
        if not transcripts or not isinstance(transcripts, list):
            # print("No transcripts found in the transcription data.")
            logger.error("No transcripts found in the transcription data.")
            return None
        # 假设只取第一个 transcript 的 text
        text = transcripts[0].get("text")
        if not text:
            # print("No text found in the transcripts.")
            logger.error("No text found in the transcripts.")
            return None

        return text

    except requests.RequestException as e:
        # print(f"Failed to download transcription file: {e}")
        logger.error(f"Failed to download transcription file: {e}")
        return None
    except ValueError as e:
        # print(f"Failed to parse transcription JSON: {e}")
        logger.error(f"Failed to parse transcription JSON: {e}")
        return None

    


if __name__ == "__main__":
    file_url = "https://ai.cytx360.com/cytxvoice/assets/hello_world_female.wav"
    voice_translation(file_url)
    
    