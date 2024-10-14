from pymongo import MongoClient
from bson.objectid import ObjectId
from AashikaMusicBot.utils.database import db  # Assuming you have a db setup

# Replace with your MongoDB connection string
MONGO_URI = "mongodb+srv://Drag:DrAg21@musicdrag.c543t.mongodb.net/?retryWrites=true&w=majority&appName=musicdrag"
client = MongoClient(MONGO_URI)
db = client["your_database_name"]
sudo_collection = db["sudo_users"]

# Load SUDO users from MongoDB
def load_sudoers():
    sudo_users = sudo_collection.find()
    return {user["user_id"] for user in sudo_users}

# Save a SUDO user to MongoDB
async def add_sudo(user_id):
    if not sudo_collection.find_one({"user_id": user_id}):
        sudo_collection.insert_one({"user_id": user_id})
        return True
    return False

# Remove a SUDO user from MongoDB
async def remove_sudo(user_id):
    result = sudo_collection.delete_one({"user_id": user_id})
    return result.deleted_count > 0

# On startup
SUDOERS = load_sudoers()

    @app.on_message(filters.command(["addsudo"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]) & filters.user(OWNER_ID))
@language
async def useradd(client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
    user = await extract_user(message)
    if user.id in SUDOERS:
        return await message.reply_text(_["sudo_1"].format(user.mention))
    added = await add_sudo(user.id)
    if added:
        SUDOERS.add(user.id)
        await message.reply_text(_["sudo_2"].format(user.mention))
    else:
        await message.reply_text(_["sudo_8"])
    # After adding a user:
    await add_sudo(user.id)

@app.on_message(filters.command(["delsudo"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]) & filters.user(OWNER_ID))
@language
async def userdel(client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
    user = await extract_user(message)
    if user.id not in SUDOERS:
        return await message.reply_text(_["sudo_3"].format(user.mention))
    removed = await remove_sudo(user.id)
    if removed:
        SUDOERS.remove(user.id)
        await message.reply_text(_["sudo_4"].format(user.mention))
    else:
        await message.reply_text(_["sudo_8"])
    # After removing a user:
    await remove_sudo(user.id)

@app.on_message(filters.command(["listsudo", "sudolist", "sudoers"]) & ~BANNED_USERS)
@language
async def sudoers_list(client, message: Message, _):
    """List all SUDO users."""
    sudo_users = sudo_collection.find()
    
    if sudo_users.count() == 0:
        await message.reply_text(_["sudo_7"])  # No SUDO users found message
        return
    
    text = _["sudo_5"]  # Base message
    user = await app.get_users(OWNER_ID)
    user_mention = user.mention if user.mention else user.first_name
    text += f"1➤ {user_mention}\n"  # Owner

    count = 1
    for sudo_user in sudo_users:
        count += 1
        user_id = sudo_user["user_id"]
        try:
            user = await app.get_users(user_id)
            user_mention = user.mention if user.mention else user.first_name
            text += f"{count}➤ {user_mention}\n"
        except Exception as e:
            continue  # If user not found, just skip

    await message.reply_text(text, reply_markup=close_markup(_))

@app.on_message(filters.command(["delallsudo"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]) & filters.user(OWNER_ID))
@language
async def del_all_sudo(client, message: Message, _):
    count = len(SUDOERS) - 1  # Exclude the admin from the count
    for user_id in SUDOERS.copy():
        if user_id != OWNER_ID:
            removed = await remove_sudo(user_id)
            if removed:
                SUDOERS.remove(user_id)
                count -= 1
    await message.reply_text(f"Removed {count} users from the sudo list.")
    sudo_collection.delete_many({})  # Clear all users
