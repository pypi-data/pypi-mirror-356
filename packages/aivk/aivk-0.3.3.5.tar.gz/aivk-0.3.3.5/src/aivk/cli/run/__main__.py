# -*- coding: utf-8 -*-
import asyncio
from logging import getLogger

from aivk.api import AivkContext
from typing import Iterator, Literal
import importlib
from click import command, option

logger = getLogger("aivk.cli.run")

def get_aivk_modules() -> Iterator[str]:
    """获取已安装的 aivk_ 开头的模块列表"""
    try:
        ctx = AivkContext.getContext()
        with ctx.env("aivk", create_venv=True):
            # 获取虚拟环境中已安装的包
            packages = ctx.list_packages("aivk")
            
            for package_info in packages:
                package_name = package_info['name']
                if package_name.startswith('aivk_'):
                    yield package_name
                    logger.info(f"发现 AIVK 模块: {package_name} ({package_info['version']})")
    except Exception as e:
        logger.error(f"获取 AIVK 模块列表失败: {e}")

def load_aivk_modules() -> None:
    """依次启动 aivk_ 开头的模块"""
    try:
        ctx = AivkContext.getContext()
        with ctx.env("aivk", create_venv=True):
            for module_name in get_aivk_modules():
                try:
                    # 导入模块
                    module = importlib.import_module(module_name)
                    
                    # 检查模块是否有启动函数
                    if hasattr(module, 'onLoad'):
                        logger.info(f"加载模块: {module_name}")
                        asyncio.run(module.onLoad())
                    elif hasattr(module, 'onUnload'):
                        logger.info(f"卸载模块: {module_name}")
                        asyncio.run(module.onUnload())
                    else:
                        logger.info(f"模块 {module_name} 已加载（无启动函数）")
                        
                except ImportError as e:
                    logger.error(f"无法导入模块 {module_name}: {e}")
                except Exception as e:
                    logger.error(f"启动模块 {module_name} 时出错: {e}")
    except Exception as e:
        logger.error(f"加载 AIVK 模块失败: {e}")

@command()
@option("--cli","style", flag_value = "cli" ,default=True, help="命令行交互方式")
@option("--web", "style", flag_value="web", help="Web 界面方式")
def run(style: Literal["cli", "web"]):    
    """
    AIVK 运行命令

    启动 AIVK CLI
    """
    try:
        print(f"AIVK 运行启动，模式: {style}")
        
        # 加载aivk_module
        print("开始加载 AIVK 模块...")
        logger.info("开始加载 AIVK 模块...")
        load_aivk_modules()
        print("AIVK 模块加载完成")
        logger.info("AIVK 模块加载完成")

        # 启动可视化界面
        match style:
            case "cli":
                print("启动命令行交互界面")
                logger.info("启动命令行交互界面")
                pass
            case "web":
                print("启动 Web 界面")
                logger.info("启动 Web 界面")
                pass
            case _:
                print(f"不支持的运行方式: {style}")
                logger.error("不支持的运行方式，请选择 'cli' 或 'web'")
                
    except Exception as e:
        print(f"运行 AIVK 时发生错误: {e}")
        logger.error(f"运行 AIVK 时发生错误: {e}")
        import traceback
        print(traceback.format_exc())