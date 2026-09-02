import os
import json
import random
import time
from google import genai
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Environment Secrets
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
BLOG_ID = os.environ.get("BLOG_ID")
GCP_SA_KEY = os.environ.get("GCP_SA_KEY")

# Gemini Client
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

# Blogger API Authenticate
sa_info = json.loads(GCP_SA_KEY)
credentials = service_account.Credentials.from_service_account_info(
    sa_info,
    scopes=['https://www.googleapis.com/auth/blogger']
)
blogger_service = build('blogger', 'v3', credentials=credentials)

# ১০টি ক্যাটাগরি
CATEGORIES = [
    "সাইবার নিরাপত্তা", "টেক রিভিউ", "পার্সোনাল ফাইন্যান্স", 
    "ট্রাভেল গাইড", "ডিজিটাল মার্কেটিং", "আর্টিফিশিয়াল ইন্টেলিজেন্স", 
    "লাইফস্টাইল", "হেলথ টিপস", "ই-কমার্স", "শিক্ষা ও ক্যারিয়ার"
]

def generate_post_with_retry(category):
    """Google Server Overload (503) সামলাতে Auto-Retry ফাংশন"""
    prompt = f"""
    Write a complete SEO-friendly blog post in Bengali for the category: '{category}'.
    Return the response STRICTLY as a valid JSON object without markdown fences.
    JSON structure:
    {{
      "title": "An engaging title in Bengali",
      "content": "HTML formatted blog content in Bengali (use <h2>, <h3>, <p> tags)"
    }}
    """
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"Trying model: gemini-2.5-flash | Attempt {attempt + 1}")
            response = gemini_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            clean_json = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_json)
        except Exception as e:
            print(f"Gemini Error on Attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                print("Server might be busy. Waiting 10 seconds before retrying...")
                time.sleep(10)
            else:
                raise e

def publish_to_blogger(post_data, category):
    body = {
        "kind": "blogger#post",
        "title": post_data["title"],
        "content": post_data["content"],
        "labels": [category]
    }
    
    posts = blogger_service.posts()
    res = posts.insert(blogId=BLOG_ID, body=body).execute()
    print(f"Successfully published to Blogger: {res.get('url')}")

def main():
    print("🚀 TechBangla AI Bot Started")
    selected_categories = random.sample(CATEGORIES, 2)
    
    for category in selected_categories:
        try:
            print(f"\nCategory: {category}")
            post_data = generate_post_with_retry(category)
            publish_to_blogger(post_data, category)
        except Exception as e:
            print(f"Failed to process category '{category}': {e}")

if __name__ == "__main__":
    main()
