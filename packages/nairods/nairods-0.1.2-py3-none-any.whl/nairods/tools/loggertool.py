# 文件名：loggertool.py
# 作者：nairoads
# 日期：2025-06-18 15:20:25
# 描述：Loguru 日志工具，支持控制台和文件日志输出

import os
from loguru import logger
import sys

# 确保日志目录存在
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 配置日志记录器
logger.remove()  # 移除默认的处理器

# 添加控制台输出处理器
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO"
)

# 添加文件处理器
logger.add(
    os.path.join(log_dir, "app_{time}.log"),
    rotation="500 MB",  # 每500MB轮换一次
    retention="10 days",  # 保留10天的日志
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="DEBUG",
    encoding="utf-8"
)

log = logger
__all__ = ["log"] 