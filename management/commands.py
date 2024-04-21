import asyncio
import sys

from task_manager.utils import get_logger

logger = get_logger(name="root", loglevel="INFO")


async def run_command(cmd):
    """
    Runs a shell command asynchronously.
    """
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    if proc.returncode != 0:
        logger.info(f'[{cmd!r} exited with {proc.returncode}]')
        if stderr:
            logger.info(f'[stderr]\n{stderr.decode()}')
    else:
        logger.info(f'[{cmd!r} exited successfully]')
        if stdout:
            sys.stdout.write(f'[stdout]\n{stdout.decode()}')


async def management_commands_before_migration():
    """
    Performs maintenance tasks before database migration asynchronously.
    """
    await run_command("bench clear-cache")
    await run_command("bench clear-website-cache")
    await run_command("bench build-search-index")