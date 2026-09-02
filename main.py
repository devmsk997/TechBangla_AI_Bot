import os
import json
import random
import time
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
from google import genai
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Environment Secrets & Fallbacks
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
BLOG_ID_OLD = os.environ.get("BLOG_ID")
BLOG_ID_NEW = os.environ.get("BLOG_ID_2") or os.environ.get("BLOG_ID_NEW")
CREDENTIALS_JSON = os.environ.get("CREDENTIALS_JSON") or os.environ.get("GOOGLE_CREDENTIALS_JSON")
TOKEN_JSON = os.environ.get("TOKEN_JSON") or os.environ.get("GOOGLE_TOKEN_JSON")

AFFILIATE_ID = "379372"

gemini_client = genai.Client(api_key=GEMINI_API_KEY)

def get_blogger_service():
    token_data = json.loads(TOKEN_JSON)
    creds = Credentials.from_authorized_user_info(token_data)
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return build('blogger', 'v3', credentials=creds)

INFO_CATEGORIES = [
    "সাইবার নিরাপত্তা", "টেক রিভিউ", "পার্সোনাল ফাইন্যান্স", 
    "ডিজিটাল মার্কেটিং", "আর্টিফিশিয়াল ইন্টেলিজেন্স"
]

AFFILIATE_PRODUCTS = [
    "Solar PTZ Security Camera", 
    "Baseus Power Bank", 
    "Wireless Earbuds", 
    "Smart Watch",
    "CC Camera",
    "Trimmer"
]

def fetch_bdstall_affiliate_link(product_name):
    """BDStall এ প্রোডাক্ট সার্চ করে অটোমেটিক অ্যাফিলিয়েট লিংক তৈরি করে"""
    try:
        search_query = urllib.parse.quote_plus(product_name)
        search_url = f"https://www.bdstall.com/search/?term={search_query}"
        
        req = urllib.request.Request(
            search_url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                if '/details/' in href:
                    if not href.startswith('http'):
                        href = "https://www.bdstall.com" + href
                    final_affiliate_link = f"{href}?ref={AFFILIATE_ID}"
                    print(f"🔗 Auto-found Affiliate Link: {final_affiliate_link}")
                    return final_affiliate_link
                    
    except Exception as e:
        print(f"⚠️ Search link fetch failed: {e}")
    
    return f"https://www.bdstall.com/?ref={AFFILIATE_ID}"

def generate_post(prompt):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = gemini_client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )
            clean_json = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_json)
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(10)
            else:
                raise e

def publish_post(blogger_service, blog_id, post_data, label):
    body = {
        "kind": "blogger#post",
        "title": post_data["title"],
        "content": post_data["content"],
        "labels": [label]
    }
    posts = blogger_service.posts()
    res = posts.insert(blogId=blog_id, body=body).execute()
    print(f"✅ Successfully published to Blog ID ({blog_id}): {res.get('url')}")

def main():
    print("🚀 Dual-Blog AI Automation Bot Started")
    blogger_service = get_blogger_service()

    # ১. পুরনো ব্লগে পোস্ট (TechBangla)
    if BLOG_ID_OLD:
        try:
            category = random.choice(INFO_CATEGORIES)
            prompt_info = f"""
            Write an SEO-friendly blog post in Bengali for category: '{category}'.
            STRICTLY return JSON with keys "title" and "content".
            The "content" must be valid HTML using <h2>, <p>, <ul> tags.
            """
            print(f"\nGenerating post for OLD blog ({BLOG_ID_OLD}): {category}")
            info_data = generate_post(prompt_info)
            publish_post(blogger_service, BLOG_ID_OLD, info_data, category)
        except Exception as e:
            print(f"❌ Old blog error: {e}")

    # ২. নতুন অ্যাফিলিয়েট ব্লগে পোস্ট (BD Tech Shop Review)
    if BLOG_ID_NEW:
        try:
            product = random.choice(AFFILIATE_PRODUCTS)
            print(f"\nSearching affiliate link for: {product}")
            affiliate_url = fetch_bdstall_affiliate_link(product)
            
            # নিখুঁত বাটনের HTML যা Gemini পরিবর্তন করবে না
            button_html = f'<p style="text-align:center; margin-top:30px;"><a href="{affiliate_url}" target="_blank" rel="sponsored" style="background-color:#28a745; color:#ffffff; padding:14px 28px; text-decoration:none; font-weight:bold; font-size:16px; border-radius:6px; display:inline-block;">👉 অর্ডার করতে এখানে ক্লিক করুন (BDStall)</a></p>'

            prompt_affiliate = f"""
            Write a high-converting Bengali affiliate product review for: '{product}'.
            Include <h2>কেন কিনবেন?</h2>, <h3>সুবিধা ও অসুবিধা</h3>.
            At the VERY END of the content, MUST append this EXACT HTML string as-is without changing any quotation marks or link:
            {button_html}

            STRICTLY return JSON format:
            {{"title": "Title in Bengali", "content": "Full HTML content including the appended button"}}
            """
            print(f"Generating review for NEW Affiliate blog ({BLOG_ID_NEW}): {product}")
            affiliate_data = generate_post(prompt_affiliate)
            
            # নিশ্চিত করা যেন বাটনটি কনটেন্টের শেষে সঠিকভাবে যুক্ত থাকে
            if affiliate_url not in affiliate_data.get("content", ""):
                affiliate_data["content"] += f"\n{button_html}"

            publish_post(blogger_service, BLOG_ID_NEW, affiliate_data, "Affiliate")
        except Exception as e:
            print(f"❌ New blog error: {e}")
    else:
        print("\n⚠️ BLOG_ID_2 / BLOG_ID_NEW secret not found!")

if __name__ == "__main__":
    main()
