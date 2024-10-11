async def edit_or_reply(message, text):
    """Edit the original message or send a reply."""
    if message.reply_to_msg_id:  # Check if the message is a reply
        await message.reply(text)
    else:
        await message.edit(text)
