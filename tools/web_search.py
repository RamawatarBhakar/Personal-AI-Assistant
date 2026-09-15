import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# 🚀 Initialize Tavily Client
if TAVILY_API_KEY:
    tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
else:
    tavily_client = None
    print("⚠️ Web Search Module Offline: Tavily key missing in .env!")

def search_the_web(query):
    """Internet se live data nikal kar lata hai"""
    if not tavily_client: 
        return "⚠️ Error: Internet connection module is offline."
    
    try:
        print(f"🌐 Searching the web for: {query}...")
        
        # AI-optimized search request
        response = tavily_client.search(
            query=query, 
            search_depth="basic", # Fast search
            max_results=3 # Top 3 most relevant results
        )
        
        # Results ko clean text me format karna
        results = response.get("results", [])
        if not results:
            return "Koi live information nahi mili."
            
        formatted_results = "\n\n".join([f"📰 Title: {r['title']}\n📄 Content: {r['content']}\n🔗 URL: {r['url']}" for r in results])
        return formatted_results
        
    except Exception as e:
        print(f"⚠️ Web Search Error: {e}")
        return f"Internet search fail ho gayi: {e}"