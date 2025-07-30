# -*- coding: utf-8 -*-
import atexit
import asyncio
from typing import Coroutine, Any, cast
from logging import getLogger
from .__about__ import __LOGO__, __BYE__
from .api import FastAIVK
logger = getLogger("aivk")
#region meta

#region aivk

@FastAIVK.aivk_metadata
class AIVK():
    """
    AIVK 元模块
    Hello AIVK!
    """
    id = "aivk"
    level : int = 0

@AIVK.onLoad
async def onLoad():
    logger.info("HELLO AIVK!")
    logger.info(__LOGO__)

@AIVK.onUnload
async def onUnload():
    logger.info("GOODBYE AIVK!")
    logger.info(__BYE__)

# 注册卸载钩子
# 注册的函数会按注册顺序的逆序执行 所以先执行aivk子模块atexit , 後执行aivk主模块atexit
def _run_onunload() -> None:
    asyncio.run(cast("Coroutine[Any, Any, None]", onUnload()))

atexit.register(_run_onunload)
