import os
import json
import random
import time
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
    "Smart Watch with SIM", "Baseus 20000mAh Power Bank", 
    "Solar PTZ Security Camera", "Wireless Earbuds", 
    "Electric Shaver for Women", "Baby Ear Wax Cleaning Kit"
]

def generate_post(prompt):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # আপডেট করা জেমিনাই মডেল ব্যবহার করা হয়েছে
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
            STRICTLY return JSON: {{"title": "Title in Bengali", "content": "HTML content using <h2>, <p>"}}
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
            prompt_affiliate = f"""
            Write a high-converting Bengali affiliate product review for: '{product}'.
            Include <h2>কেন কিনবেন?</h2>, <h3>সুবিধা ও অসুবিধা</h3>. 
            Add a green button at the bottom: '<div style="text-align:center; margin-top:20px;"><a href="#" style="background-color:#28a745; color:white; padding:12px 25px; text-decoration:none; font-weight:bold; border-radius:5px;">অর্ডার করতে এখানে ক্লিক করুন (BDStall)</a></div>'
            STRICTLY return JSON: {{"title": "Title in Bengali", "content": "HTML content"}}
            """
            print(f"\nGenerating review for NEW Affiliate blog ({BLOG_ID_NEW}): {product}")
            affiliate_data = generate_post(prompt_affiliate)
            publish_post(blogger_service, BLOG_ID_NEW, affiliate_data, "Affiliate")
        except Exception as e:
            print(f"❌ New blog error: {e}")
    else:
        print("\n⚠️ BLOG_ID_2 / BLOG_ID_NEW secret not found!")

if __name__ == "__main__":
    main()
