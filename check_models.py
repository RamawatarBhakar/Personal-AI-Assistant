from groq import Groq
from config.settings import GROQ_API_KEY

try:
    client = Groq(api_key=GROQ_API_KEY)
    print("🔥 Groq par is waqt Zinda (Active) Models ki List:\n")
    
    # Ye API se live models ki list nikalega
    models = client.models.list()
    for model in models.data:
        print(f"✅ {model.id}")
        
except Exception as e:
    print(f"❌ Error: {e}")