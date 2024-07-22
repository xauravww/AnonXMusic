import asyncio
import importlib
import threading
import time
from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall
from AnonXMusic.server import server  # Import the server function from server.py
import config
from cron import hit_server_url

from AnonXMusic import LOGGER, app, userbot
from AnonXMusic.core.call import Anony
from AnonXMusic.misc import sudo
from AnonXMusic.plugins import ALL_MODULES
from AnonXMusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS

# Define a function to run the server URL hitting in a separate thread
def run_server_url():
    while True:
        try:
            hit_server_url()
        except Exception as e:
            LOGGER(__name__).error(f"Error hitting server URL: {str(e)}")
        # Sleep for a specified duration before hitting the server URL again
        time.sleep(13 * 60)  # Sleep for 13 minutes

async def init():
    try:
        if (
            not config.STRING1
            and not config.STRING2
            and not config.STRING3
            and not config.STRING4
            and not config.STRING5
        ):
            LOGGER(__name__).error("Assistant client variables not defined, exiting...")
            return
        
        await sudo()
        
        try:
            users = await get_gbanned()
            for user_id in users:
                BANNED_USERS.add(user_id)
            users = await get_banned_users()
            for user_id in users:
                BANNED_USERS.add(user_id)
        except Exception as e:
            LOGGER(__name__).error(f"Error loading banned users: {str(e)}")
        
        await app.start()
        
        for all_module in ALL_MODULES:
            importlib.import_module("AnonXMusic.plugins" + all_module)
        
        LOGGER("AnonXMusic.plugins").info("Successfully Imported Modules...")
        
        await userbot.start()
        await Anony.start()
        
        try:
            await Anony.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
        except NoActiveGroupCall:
            LOGGER("AnonXMusic").error(
                "Please turn on the videochat of your log group/channel.\n\nStopping Bot..."
            )
        except Exception as e:
            LOGGER("AnonXMusic").error(f"Error starting stream call: {str(e)}")
        
        await Anony.decorators()
        LOGGER("AnonXMusic").info("AnonX Music Bot Started Successfully.")
        
        await idle()
        
    except Exception as e:
        LOGGER(__name__).error(f"Error in init function: {str(e)}")
        
    finally:
        await app.stop()
        await userbot.stop()
        LOGGER("AnonXMusic").info("Stopping AnonX Music Bot...")

if __name__ == "__main__":
    # Start the server URL hitting function in a separate thread
    server_url_thread = threading.Thread(target=run_server_url)
    server_url_thread.start()

    # Start the server in a separate thread
    server_thread = threading.Thread(target=server)
    server_thread.start()
    
    asyncio.get_event_loop().run_until_complete(init())
    
    # Wait for the server thread to finish
    server_thread.join()
