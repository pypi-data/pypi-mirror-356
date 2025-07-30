# -*- coding: utf-8 -*-
import asyncio
from logging import getLogger , basicConfig , DEBUG , INFO, WARNING, ERROR
from aivk.api import AivkContext, AivkFS , AivkLoader , AivkMod
from click import command, pass_context , Context

logger = getLogger("aivk.cli.run")
@command()
@pass_context
def run(ctx: Context):
    """
    AIVK 运行命令
    :param style: 运行方式，支持 "cli" 或 "web"
    启动 AIVK CLI
    """
    verbose = ctx.obj["verbose"]
    match verbose:
        case 0:
            # -v: 不显示任何日志
            basicConfig(level=ERROR)
            logger.info(f"日志级别设置为 ERROR (verbose={verbose}) - 不显示任何日志")
        case 3:
            # -vvv: 显示所有日志（DEBUG 及以上）
            basicConfig(level=DEBUG)
            logger.info(f"日志级别设置为 DEBUG (verbose={verbose}) - 显示所有调试信息")
        case 2:
            # -vv: 显示详细信息（INFO 及以上）
            basicConfig(level=INFO)
            logger.info(f"日志级别设置为 INFO (verbose={verbose}) - 显示详细信息")
        case 1:
            # -v: 显示重要信息（INFO 及以上，但减少部分详细输出）
            basicConfig(level=WARNING)
            logger.info(f"日志级别设置为 WARNING (verbose={verbose}) - 显示重要信息")
        case _:
            # 这里不应该执行到
            basicConfig(level=INFO)
            logger.info(f"日志级别设置为 INFO (verbose={verbose}) - 显示详细信息")

    async def run():
        try:
            # 加载aivk_module
            logger.info("开始加载 AIVK 模块...")
            ctx = AivkContext.getContext()

            async with ctx.env("aivk", create_venv=True) as fs:
                loader = AivkLoader.getLoader()
                aivk_modules = await loader.ls(fs)  # 获取所有 AIVK 模块列表
                # 自加载 
                await loader.load(fs, "aivk", aivk_modules)  # 加载 AIVK 模块
                # 加载其他组件 -- 如果未禁用
                await loader.load(fs, "*", aivk_modules)  # 加载其他所有组件
                AivkLoader.aivk_box.to_toml(AivkFS.aivk_cache / "aivk_box.toml")  # type: ignore
                # 开始执行
                await AivkMod.exec("aivk", "onLoad")  # 执行 AIVK 的 onLoad 钩子
                await AivkMod.exec("web", "onLoad")  # 执行 Web 的 onLoad 钩子

        except Exception as e:
            logger.error(f"运行 AIVK 时发生错误: {e}")
            import traceback
            logger.error(traceback.format_exc(limit=20))

    asyncio.run(run())