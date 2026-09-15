from groq import Groq
import google.generativeai as genai
import json
from datetime import datetime # ⏱️ Time Module
from config.settings import GROQ_API_KEY, GEMINI_API_KEY
from database.redis_db import get_chat_history, save_chat_history
from database.qdrant_db import search_long_term_memory
from tools.web_search import search_the_web
from tools.stealth_read import read_webpage # 📖 Jina AI Tool
import config.state as state

# 1. Initialize Engines
groq_client = Groq(api_key=GROQ_API_KEY)
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel('gemini-1.5-flash')

# 2. AI ke dono Hathiyar (Internet & Scraper)
jarvis_tools = [
    {
        "type": "function",
        "function": {
            "name": "search_the_web",
            "description": "Get real-time news, weather, live sports scores, stock prices, and current facts from the internet.",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string", "description": "The exact search query to look up."}},
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_webpage",
            "description": "Scrape and read the full text content of a specific webpage URL.",
            "parameters": {
                "type": "object",
                "properties": {"url": {"type": "string", "description": "The exact URL link to read."}},
                "required": ["url"],
            },
        },
    }
]

def get_ai_response(user_id, user_message):
    
    # 🟢 STEP 1: Live Digital Clock & Personality (SABSE UPAR)
    current_time = datetime.now().strftime("%A, %B %d, %Y %I:%M %p")
    base_prompt = f"You are JARVIS, a highly advanced personal AI assistant. Reply like a pro. Keep answers concise. IMPORTANT: Today's current date and time is {current_time}. Always use this date for 'today' or 'recent' context."
    
    # 🟢 STEP 2: Permanent Vault (Qdrant) se purani memory nikalna
    vault_context = search_long_term_memory(user_message)
    if vault_context:
        base_prompt += f"\n\nHere is some long-term memory context about the user:\n{vault_context}"
        
    system_prompt = {"role": "system", "content": base_prompt}
    
    # 🟢 STEP 3: Short-term memory (Redis) lana (Last 6 messages)
    history = get_chat_history(user_id, limit=6)
    messages = [system_prompt] + history + [{"role": "user", "content": user_message}]
    
    # Tera active CHAT model
    current_model = "qwen/qwen3.8-27b"
    
    try:
        # 🟢 STEP 4: Primary Engine (Groq) Call
        if state.is_secure_mode:
            # 🔒 GHOST MODE: Bina kisi tool ke call karna (100% Private)
            response = groq_client.chat.completions.create(
                messages=messages,
                model=current_model
            )
        else:
            # 🌐 NORMAL MODE: Internet tools ke sath call karna
            response = groq_client.chat.completions.create(
                messages=messages,
                model=current_model,
                tools=jarvis_tools,
                tool_choice="auto" 
            )
        
        response_message = response.choices[0].message
        
        # 🟢 STEP 5: Agar AI ne tool use karne ka faisla kiya
        if response_message.tool_calls:
            messages.append(response_message) # Push AI's tool request to history
            
            for tool_call in response_message.tool_calls:
                args = json.loads(tool_call.function.arguments)
                
                # Check kaunsa tool manga gaya hai
                if tool_call.function.name == "search_the_web":
                    search_query = args.get("query")
                    print(f"🔍 JARVIS is searching the web for: {search_query}")
                    tool_result = search_the_web(search_query)
                    
                elif tool_call.function.name == "read_webpage":
                    target_url = args.get("url")
                    print(f"📖 JARVIS is reading URL: {target_url}")
                    tool_result = read_webpage(target_url)
                else:
                    tool_result = "Tool not found."
                
                # Result wapas AI ko dena
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": tool_call.function.name,
                    "content": tool_result
                })
            
            # 🟢 STEP 6: Tool ka data milne ke baad Final Answer banana
            final_response = groq_client.chat.completions.create(
                messages=messages,
                model=current_model
            )
            response_text = final_response.choices[0].message.content
            
        else:
            response_text = response_message.content

        # Cloud me baatcheet save karna
        save_chat_history(user_id, "user", user_message)
        save_chat_history(user_id, "assistant", response_text)
        
        return response_text
        
    except Exception as groq_error:
        print(f"⚠️ Primary Engine (Groq) Failed: {groq_error}. Switching to Fallback...")
        
        # 🟡 STEP 7: The Gemini Fallback
        try:
            if not GEMINI_API_KEY:
                return "⚠️ Boss, Groq fail ho gaya aur Gemini API key missing hai!"
            
            history_text = "\n".join([f"{m['role']}: {m['content']}" for m in history])
            prompt = f"{base_prompt}\n\nChat History:\n{history_text}\n\nUser: {user_message}"
            
            response = gemini_model.generate_content(prompt)
            
            save_chat_history(user_id, "user", user_message)
            save_chat_history(user_id, "assistant", response.text)
            
            return response.text
            
        except Exception as gemini_error:
            return f"❌ Boss, dono engines down hain! Groq: {groq_error} | Gemini: {gemini_error}"