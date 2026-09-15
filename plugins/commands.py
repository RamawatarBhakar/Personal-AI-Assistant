from pyrogram import Client, filters
from config.settings import ADMIN_ID
from database.qdrant_db import save_long_term_memory
import config.state as state # 🚀 Naya Import: State track karne ke liye

# 🟢 1. /start Command (Basic Greeting)
@Client.on_message(filters.command("start"))
async def start_command(client, message):
    print(f"👀 GUEST ALERT: Message received from User ID -> {message.from_user.id}")
    await message.reply_text("🤖 Hello Boss! JARVIS is online and ready for your commands.")

# 🟡 2. /ping Command (Server Health Check)
@Client.on_message(filters.command("ping") & filters.user(ADMIN_ID))
async def ping_command(client, message):
    await message.reply_text("🏓 Pong! Cloud-Native infrastructure is perfectly stable.")

# 🔴 3. /remember Command (The Permanent Vault)
@Client.on_message(filters.command("remember") & filters.user(ADMIN_ID))
async def remember_command(client, message):
    # Check karna ki command ke aage kuch likha hai ya nahi
    if len(message.command) > 1:
        # "/remember " ke baad ka poora text nikalna
        memory_text = message.text.split(None, 1)[1]
        
        # Qdrant me save karna
        success = save_long_term_memory(memory_text)
        
        if success:
            await message.reply_text(f"✅ Boss, maine permanent vault me encrypt karke save kar liya hai:\n\n'{memory_text}'")
        else:
            await message.reply_text("❌ System Error: Memory save nahi ho payi. Logs check karein.")
    else:
        await message.reply_text("⚠️ Boss, command ke aage wo likho jo yaad rakhna hai.\nExample: `/remember Meri favorite car Porsche 911 hai`")


        # 🥷 4. /secure Command (Ghost Mode Toggle)
@Client.on_message(filters.command("secure") & filters.user(ADMIN_ID))
async def secure_command(client, message):
    # Mode ko flip karna (True hai toh False, False hai toh True)
    state.is_secure_mode = not state.is_secure_mode
    
    if state.is_secure_mode:
        await message.reply_text("🔒 **GHOST MODE ON:** Internet tools and scraping disabled. 100% private local processing active.")
    else:
        await message.reply_text("🌐 **GHOST MODE OFF:** Internet access restored. JARVIS is connected to the world.")