# -*- coding: utf-8 -*-
import atexit
from .api import FastAIVK
from .__about__ import __LOGO__, __BYE__

from logging import getLogger
logger = getLogger("aivk")

@FastAIVK.aivk_metadata
class META():
    """
    AIVK 元数据
    """
    id = "aivk"
    level : int = 0

async def onLoad():
    logger.info("HELLO AIVK!")
    logger.info(__LOGO__)

def onUnload():
    logger.info("GOODBYE AIVK!")
    logger.info(__BYE__)

# 注册卸载钩子
# 注册的函数会按注册顺序的逆序执行 所以先执行aivk子模块atexit , 后执行aivk主模块atexit
atexit.register(onUnload)