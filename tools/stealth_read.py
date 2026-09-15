import requests

def read_webpage(url):
    """Kisi bhi URL ke andar ka poora content padhne ke liye"""
    try:
        print(f"📖 JARVIS is reading webpage: {url}...")
        # Jina AI URL ko saaf text mein badal deta hai bina ads ke
        response = requests.get(f"https://r.jina.ai/{url}")
        
        if response.status_code == 200:
            # Token limit bachane ke liye sirf shuruwat ka important data bhejenge
            return response.text[:5000] 
        else:
            return "⚠️ Error: Webpage read nahi ho paya."
    except Exception as e:
        print(f"⚠️ Jina AI Error: {e}")
        return f"Scraping failed: {e}"