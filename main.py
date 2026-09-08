import os
import json
import time
import re
from google import genai
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# SEO & Bot Modules Import
from topic_cluster import choose_topic, save_topic
from keyword_research import research_keywords
from gemini_writer import generate_article
from seo_optimizer import optimize_seo
from duplicate_checker import check_duplicate
from image_generator import generate_image
from quality_score import calculate_quality_score
from blogger import create_json_ld, save_post

# Environment Variables
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
BLOG_ID = os.environ.get("BLOG_ID")
CREDENTIALS_JSON = os.environ.get("GOOGLE_CREDENTIALS_JSON") or os.environ.get("CREDENTIALS_JSON")
TOKEN_JSON = os.environ.get("GOOGLE_TOKEN_JSON") or os.environ.get("TOKEN_JSON")

def get_blogger_service():
    token_data = json.loads(TOKEN_JSON)
    creds = Credentials.from_authorized_user_info(token_data)
    if creds and creds.expired and creds.refresh_token:
        client_data = json.loads(CREDENTIALS_JSON)
        creds.refresh(Request())
    return build('blogger', 'v3', credentials=creds)

def parse_gemini_output(generated_text):
    title_match = re.search(r"TITLE:\s*(.*?)\n", generated_text, re.IGNORECASE)
    desc_match = re.search(r"SEARCH_DESCRIPTION:\s*(.*?)\n", generated_text, re.IGNORECASE)
    labels_match = re.search(r"LABELS:\s*(.*?)\n", generated_text, re.IGNORECASE)
    content_match = re.search(r"CONTENT:\s*(.*)", generated_text, re.DOTALL | re.IGNORECASE)

    title = title_match.group(1).strip() if title_match else "TechBangla Technology Guide"
    search_description = desc_match.group(1).strip() if desc_match else ""
    
    labels_raw = labels_match.group(1).strip() if labels_match else ""
    labels = [label.strip() for label in labels_raw.split(",") if label.strip()]
    
    content = content_match.group(1).strip() if content_match else generated_text
    return title, search_description, labels, content

def main():
    print("🚀 TechBangla SEO Auto-Post Bot Started")
    
    # ১. Topic & Category Selection
    topic, category = choose_topic()
    print(f"📌 Topic: {topic} | Category: {category}")

    # ২. Keyword Research
    keywords = research_keywords(category, topic)
    print(f"🔑 Keywords: {keywords}")

    # ৩. Article Generation (gemini_writer স্বয়ংক্রিয়ভাবে blog_posts.json থেকে আসল লিংক যোগ করবে)
    raw_article = generate_article(topic, category, keywords)
    title, search_description, labels, content = parse_gemini_output(raw_article)

    # ৪. Duplicate Check
    dup_res = check_duplicate(title, content)
    if dup_res.get("duplicate"):
        print(f"⚠️ Duplicate detected ({dup_res.get('similarity')}% similarity). Skipping generation.")
        return

    # ৫. Quality & SEO Check
    q_score = calculate_quality_score(title, content)
    print(f"📊 Quality Score: {q_score['score']}/100")

    # ৬. Image Generation
    try:
        img_url = generate_image(title)
        print(f"🖼️ Final Image URL for Blogger: {img_url}")
    except Exception as e:
        print(f"⚠️ Image generation skipped: {e}")
        img_url = "https://images.unsplash.com/photo-1518770660439-4636190af475?w=1280&auto=format&fit=crop"

    # ৭. SEO Optimization Payload
    seo_data = optimize_seo(title, content, category)
    if not search_description:
        search_description = seo_data.get("search_description", "")
        
    # সার্চ ডেসক্রিপশন সর্বোচ্চ ১৫০ অক্ষরে সীমাবদ্ধ রাখা
    search_description = search_description[:150]

    # ৮. Format Content with Schema & Responsive Blogger Featured Image
    try:
        schema = create_json_ld(title, search_description, img_url)
    except Exception:
        schema = ""
        
    image_html = ""
    if img_url:
        image_html = f'''
<div class="separator" style="clear: both; text-align: center; margin-bottom: 25px;">
    <a href="{img_url}" style="margin-left: auto; margin-right: auto; display: block;">
        <img border="0" src="{img_url}" alt="{title}" title="{title}" loading="eager" style="max-width:100%; width:100%; height:auto; object-fit:cover; border-radius:8px;" />
    </a>
</div>
<br/>
'''
    final_content = schema + image_html + content

    # ৯. Publish to Blogger
    blogger_service = get_blogger_service()
    body = {
        "kind": "blogger#post",
        "title": title,
        "content": final_content,
        "labels": labels if labels else [category],
        "searchDescription": search_description
    }

    res = blogger_service.posts().insert(blogId=BLOG_ID, body=body, isDraft=False).execute()
    published_url = res.get('url')
    print(f"✅ Successfully Published: {published_url}")
    
    # ১০. Save Post & Topic Data (Blogger থেকে পাওয়া আসল URL সেভ করা হচ্ছে)
    try:
        save_post(title, published_url, category)
        save_topic(topic)
        print("💾 Post and Topic history saved successfully.")
    except Exception as e:
        print(f"⚠️ Failed to save post history: {e}")

if __name__ == "__main__":
    main()
