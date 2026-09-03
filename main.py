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
HISTORY_FILE = "posted_history.json"

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

def load_posted_history():
    """পূর্বে পোস্ট করা প্রোডাক্টের নাম লোড করে"""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_posted_history(history):
    """নতুন পোস্ট হওয়া প্রোডাক্ট সেভ করে"""
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"⚠️ History save error: {e}")

def fetch_bdstall_details(product_name):
    """BDStall থেকে অটোমেটিক অ্যাফিলিয়েট লিংক এবং প্রোডাক্টের ছবি স্ক্র্যাপ করে"""
    fallback_image = "https://images.unsplash.com/photo-1526738549149-8e07eca6c147?w=800&auto=format&fit=crop"
    
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
                    
                    # ছবি স্ক্র্যাপ করা
                    img_tag = a_tag.find('img')
                    image_url = fallback_image
                    if img_tag:
                        image_url = img_tag.get('src') or img_tag.get('data-src') or fallback_image
                        if image_url and not image_url.startswith('http'):
                            image_url = "https://www.bdstall.com" + image_url
                            
                    print(f"🔗 Found Affiliate Link: {final_affiliate_link}")
                    print(f"🖼️ Found Image URL: {image_url}")
                    return final_affiliate_link, image_url
                    
    except Exception as e:
        print(f"⚠️ Search details fetch failed: {e}")
    
    return f"https://www.bdstall.com/?ref={AFFILIATE_ID}", fallback_image

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
    history = load_posted_history()

    # ১. পুরোনো ব্লগে পোস্ট (TechBangla)
    if BLOG_ID_OLD:
        try:
            category = random.choice(INFO_CATEGORIES)
            
            # স্থায়ী ফিক্সড ক্যাটাগরি ইমেজ ম্যাপিং (রিফ্রেশ করলেও পরিবর্তন হবে না)
            category_images = {
                "সাইবার নিরাপত্তা": "https://images.unsplash.com/photo-1563986768609-322da13575f3?w=800&auto=format&fit=crop",
                "টেক রিভিউ": "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=800&auto=format&fit=crop",
                "পার্সোনাল ফাইন্যান্স": "https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=800&auto=format&fit=crop",
                "ডিজিটাল মার্কেটিং": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&auto=format&fit=crop",
                "আর্টিফিশিয়াল ইন্টেলিজেন্স": "https://images.unsplash.com/photo-1677442136019-21780efad99a?w=800&auto=format&fit=crop"
            }
            
            info_image_url = category_images.get(category, "https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&auto=format&fit=crop")
            info_image_html = f'<div class="separator" style="clear: both; text-align: center; margin-bottom: 20px;"><img border="0" src="{info_image_url}" alt="{category}" style="max-width:100%; height:auto;" /></div>\n\n'

            prompt_info = f"""
            Write an SEO-friendly blog post in Bengali for category: '{category}'.
            STRICTLY return JSON with keys "title" and "content".
            The "content" must be valid HTML using <h2>, <p>, <ul> tags.
            """
            print(f"\nGenerating post for OLD blog ({BLOG_ID_OLD}): {category}")
            info_data = generate_post(prompt_info)
            
            # কন্টেন্টের শুরুতে স্থায়ী ফিচার ছবি যুক্ত করা
            info_data["content"] = info_image_html + info_data["content"]
            
            publish_post(blogger_service, BLOG_ID_OLD, info_data, category)
        except Exception as e:
            print(f"❌ Old blog error: {e}")

    # ২. নতুন অ্যাফিলিয়েট ব্লগে পোস্ট (BD Tech Shop Review)
    if BLOG_ID_NEW:
        try:
            # ডুপ্লিকেট এড়াতে না পোস্ট হওয়া প্রোডাক্ট ফিল্টার করা
            available_products = [p for p in AFFILIATE_PRODUCTS if p not in history]
            
            # সব প্রোডাক্ট পোস্ট হয়ে গেলে লিস্ট রিসেট হবে
            if not available_products:
                available_products = AFFILIATE_PRODUCTS
                history = []

            product = random.choice(available_products)
            print(f"\nSearching affiliate details for: {product}")
            affiliate_url, image_url = fetch_bdstall_details(product)
            
            # ১. একদম শুরুতে ফিচার ইমেজের HTML
            feature_image_html = f'<div class="separator" style="clear: both; text-align: center; margin-bottom: 25px;"><a href="{affiliate_url}" target="_blank" rel="sponsored"><img border="0" src="{image_url}" alt="{product}" style="max-width:100%; height:auto; border-radius:8px;" /></a></div>\n\n'

            # ২. শেষে বাই বাটনের HTML
            button_html = f'<p style="text-align:center; margin-top:30px;"><a href="{affiliate_url}" target="_blank" rel="sponsored" style="background-color:#28a745; color:#ffffff; padding:14px 28px; text-decoration:none; font-weight:bold; font-size:16px; border-radius:6px; display:inline-block;">👉 অর্ডার করতে এখানে ক্লিক করুন (BDStall)</a></p>'

            prompt_affiliate = f"""
            Write a high-converting Bengali affiliate product review for: '{product}'.
            Include <h2>কেন কিনবেন?</h2>, <h3>সুবিধা ও অসুবিধা</h3>.

            STRICTLY return JSON format:
            {{"title": "Title in Bengali", "content": "Full HTML content"}}
            """
            print(f"Generating review for NEW Affiliate blog ({BLOG_ID_NEW}): {product}")
            affiliate_data = generate_post(prompt_affiliate)
            
            # ইমেজ ও বাটন কনটেন্টের সাথে সঠিকভাবে কম্বাইন করা হলো
            final_content = feature_image_html + affiliate_data.get("content", "") + f"\n{button_html}"
            affiliate_data["content"] = final_content

            publish_post(blogger_service, BLOG_ID_NEW, affiliate_data, "Affiliate")
            
            # হিস্ট্রিতে সেভ করা
            history.append(product)
            save_posted_history(history)
            
        except Exception as e:
            print(f"❌ New blog error: {e}")
    else:
        print("\n⚠️ BLOG_ID_2 / BLOG_ID_NEW secret not found!")

if __name__ == "__main__":
    main()
