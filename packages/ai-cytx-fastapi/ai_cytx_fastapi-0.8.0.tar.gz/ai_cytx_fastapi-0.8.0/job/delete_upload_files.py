from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime,timedelta
import os
from config.settings import upload_folder
import logging

logger = logging.getLogger(__name__)

def job():
    try:
        print(f"任务执行时间: {datetime.now()}")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
        target_dir = os.path.join(upload_folder, yesterday)

        logger.info(f"开始清理目录: {target_dir}")

        if not os.path.exists(target_dir):
            logger.warning(f"目录不存在: {target_dir}")
            return

        # 遍历并删除文件
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
                logger.info(f"已删除文件: {file_path}")
        logger.info(f"清理完成: {target_dir}")
    except Exception as e:
        logger.error(f"清理任务出错: {e}", exc_info=True)

