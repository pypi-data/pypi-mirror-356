from click import group , option, pass_context , Context
from aivk.cli.amcp import aivk_mcp
from aivk.cli.list import aivk_list
from aivk.cli.install import install
from aivk.cli.uninstall import uninstall
from aivk.cli.run import run
from aivk.base.aivk import AivkMod
debug = AivkMod.getMod("aivk")

@group() 
@option("-v", "--verbose", count=True, default=2, help="详细程度，可以多次使用 (-v, -vv, -vvv)")
@pass_context
def cli(ctx: Context, verbose: int):
    """
    AIVK CLI
    """
    verbose = min(verbose, 3)  # 限制 verbose 最大值为 3
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose

cli.add_command(aivk_mcp)
cli.add_command(aivk_list)
cli.add_command(install)
cli.add_command(uninstall)
cli.add_command(run)

cli.add_command(debug, name="debug")
