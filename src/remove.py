import config
import asyncio
from discord_slash.utils import manage_commands


try:
    from local_settings import *

    LOCAL_HOST = True
except ImportError:
    import keep_alive

    keep_alive.keep_alive()


async def remove():
    await manage_commands.remove_all_commands_in(config.bot_id, TOKEN, config.guild_ids)
    print("remove sucsess")


asyncio.run(remove())
