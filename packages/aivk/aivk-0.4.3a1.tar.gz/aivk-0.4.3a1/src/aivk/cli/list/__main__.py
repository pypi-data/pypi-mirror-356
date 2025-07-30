# -*- coding: utf-8 -*-
from logging import getLogger
from click import command, option

logger = getLogger("aivk.cli.list")

@command("list")
@option("-v", "--verbose", count=True,default=1 , help="增加详细程度 (-v INFO, -vv DEBUG, -vvv 显示所有包详情)")
def aivk_list(verbose: int):
    """
    列出所有已安装的 AIVK 模块
    """
    # 根据 verbose 级别配置日志
    pass 