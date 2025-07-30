from click import command, option, argument
from logging import getLogger

logger = getLogger("aivk.cli.install")
@command()
@argument('package', required=True)
@option('--env-id', '-e', default='aivk', help='目标虚拟环境ID (默认: aivk)')
@option('--upgrade', '-U', is_flag=True, help='升级包到最新版本')
@option('--force-reinstall', is_flag=True, help='强制重新安装')
@option('--no-deps', is_flag=True, help='不安装依赖')
@option('--editable', '-E', is_flag=True, help='以可编辑模式安装 (仅限本地路径)')
def install(package: str, env_id: str, upgrade: bool, force_reinstall: bool, no_deps: bool, editable: bool):
    """
    AIVK 安装命令
    
    安装指定的包到AIVK虚拟环境中
    
    PACKAGE 可以是:
    - PyPI包名: numpy, pandas, requests
    - GitHub仓库: https://github.com/user/repo.git 或 git+https://github.com/user/repo.git
    - 本地路径: ./path/to/package 或 /absolute/path/to/package
    """
    pass