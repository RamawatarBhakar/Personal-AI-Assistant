from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from config.settings import ADMIN_ID
from ai_engine.router import get_ai_response 

# 🧠 AI CHAT ENGINE (Sirf Admin ke liye)
# 🚀 FIX: ~filters.regex(r"^/") add kiya taaki yeh kisi bhi '/' wali command ko hijack na kare
@Client.on_message(filters.text & ~filters.regex(r"^/") & filters.user(ADMIN_ID))
async def chat_with_jarvis(client, message):
    
    # Jab tak AI soch raha hai, Telegram par "typing..." dikhega
    await client.send_chat_action(message.chat.id, ChatAction.TYPING)
    
    # Tere message ko AI ke paas bhej kar answer lana
    ai_reply = get_ai_response(message.from_user.id, message.text)
    
    # JARVIS ka final reply
    await message.reply_text(ai_reply)


# 👻 GHOST MODE (Dusro ko silently ignore karega)
@Client.on_message(filters.text & ~filters.user(ADMIN_ID))
async def ignore_strangers(client, message):
    print(f"⚠️ Unauthorized ping by ID: {message.from_user.id}")