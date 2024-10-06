import psutil
import subprocess
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

# Replace with your owner ID
OWNER_ID = 7058357442  # Your Telegram user ID

def get_system_stats():
    # Get uptime
    uptime = subprocess.check_output("uptime -p", shell=True).decode().strip()
    
    # Get RAM usage
    ram = psutil.virtual_memory()
    ram_info = f"Total: {ram.total / (1024 ** 2):.2f} MB, Used: {ram.used / (1024 ** 2):.2f} MB, Free: {ram.free / (1024 ** 2):.2f} MB"
    
    # Get CPU usage
    cpu_usage = psutil.cpu_percent(interval=1)
    
    # Get disk usage
    disk = psutil.disk_usage('/')
    disk_info = f"Total: {disk.total / (1024 ** 3):.2f} GB, Used: {disk.used / (1024 ** 3):.2f} GB, Free: {disk.free / (1024 ** 3):.2f} GB"
    
    # Get Py-TgCalls status (Example, adjust as needed)
    tg_calls_status = "Running"  # Replace with actual check if necessary
    
    return f"**System Stats:**\n\n" \
           f"**Uptime:** {uptime}\n" \
           f"**RAM:** {ram_info}\n" \
           f"**CPU Usage:** {cpu_usage}%\n" \
           f"**Disk Usage:** {disk_info}\n" \
           f"**Py-TgCalls Status:** {tg_calls_status}"

def ping(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id == OWNER_ID:
        stats = get_system_stats()
        update.message.reply_text(stats, parse_mode='Markdown')
    else:
        update.message.reply_text("You do not have permission to use this command.")

# In your bot's main file, add the command handler
# Assuming you have an `updater` instance already set up
updater.dispatcher.add_handler(CommandHandler("ping", ping))
