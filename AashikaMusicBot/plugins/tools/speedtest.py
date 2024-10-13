import asyncio
import speedtest
import logging
from pyrogram import filters
from pyrogram.types import Message

from AashikaMusicBot import app
from AashikaMusicBot.misc import SUDOERS
from AashikaMusicBot.utils.decorators.language import language

#logging        
logging.basicConfig(level=logging.DEBUG)



def testspeed(m, _):
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        m.edit_text(_["server_12"])  # Update message to indicate server selection
        test.download()
        m.edit_text(_["server_13"])  # Update message to indicate download test
        test.upload()
        test.results.share()  # Share the results for a public link
        m.edit_text(_["server_14"])  # Update message to indicate completion
        return test.results.dict()  # Return the results
    except Exception as e:
        return m.edit_text(f"<code>{e}</code>")  # Return error message


@app.on_message(filters.command(["speedtest", "spt", "st"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]) & SUDOERS)
@language 
async def speedtest_function(client, message: Message, _):
    m = await message.reply_text(_["server_11"])  # Initial message indicating the start of the test
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, testspeed, m, _)  # Run testspeed in a separate thread

    if isinstance(result, dict):  # Ensure result is a dictionary
        output = _["server_15"].format(
            result["client"]["isp"],
            result["client"]["country"],
            result["server"]["name"],
            result["server"]["country"],
            result["server"]["cc"],
            result["server"]["sponsor"],
            result["server"]["latency"],
            result["ping"],
        )
        msg = await message.reply_photo(photo=result["share"], caption=output)  # Send the results as a photo
    else:
        await m.edit_text(result)  # Edit the initial message to show error
    await m.delete()  # Delete the initial message

test = speedtest.Speedtest()
print(test.get_best_server())
