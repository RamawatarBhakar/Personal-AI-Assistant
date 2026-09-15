import os
import json
from upstash_redis import Redis
from dotenv import load_dotenv

load_dotenv()

UPSTASH_URL = os.getenv("UPSTASH_REDIS_REST_URL")
UPSTASH_TOKEN = os.getenv("UPSTASH_REDIS_REST_TOKEN")

# Initialize Redis Connection
if UPSTASH_URL and UPSTASH_TOKEN:
    redis = Redis(url=UPSTASH_URL, token=UPSTASH_TOKEN)
else:
    redis = None
    print("⚠️ Memory Module Offline: Upstash keys missing in .env!")

def get_chat_history(user_id, limit=6):
    """Pichle messages cloud se nikal kar layega"""
    if not redis: return []
    try:
        raw_data = redis.lrange(f"chat:{user_id}", 0, limit - 1)
        # Data JSON string format me aata hai, usko wapas dictionary me convert karna
        return [json.loads(msg) for msg in raw_data][::-1] # Chronological order ke liye reverse kiya
    except Exception as e:
        print(f"⚠️ Memory fetch error: {e}")
        return []

def save_chat_history(user_id, role, content, limit=6):
    """Naye messages ko cloud me push karega aur limit maintain karega"""
    if not redis: return
    try:
        msg = json.dumps({"role": role, "content": content})
        key = f"chat:{user_id}"
        
        # Naya message aage add karo
        redis.lpush(key, msg)
        # Sirf latest 'limit' messages ko bacha kar baaki delete kar do (Space saving)
        redis.ltrim(key, 0, limit - 1)
    except Exception as e:
        print(f"⚠️ Memory save error: {e}")