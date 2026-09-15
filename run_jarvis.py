from pyrogram import Client
from config.settings import API_ID, API_HASH, BOT_TOKEN

# 🚀 Smart Pyrogram Setup: Ye auto-detect karega 'plugins' folder ko!
app = Client(
    "JarvisBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins") # Saare handlers yahan se load honge
)

if __name__ == "__main__":
    print("🚀 JARVIS V5.0 Engine Booting Up (Modular Mode)...")
    app.run()