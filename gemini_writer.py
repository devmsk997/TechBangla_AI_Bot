import os
import json
import time
from google import genai
from google.genai import types

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def get_recent_internal_links():
    """
    blog_posts.json থেকে আসল ৩টি পোস্টের অরিজিনাল লিংক নিয়ে HTML লিস্ট তৈরি করে।
    """
    try:
        if os.path.exists('blog_posts.json'):
            with open('blog_posts.json', 'r', encoding='utf-8') as f:
                posts = json.load(f)
            
            # শুধুমাত্র বৈধ URL আছে এমন সাম্প্রতিক ৩টি পোস্ট নেওয়া
            valid_posts = [p for p in posts if isinstance(p, dict) and p.get('url')]
            recent_posts = valid_posts[-3:]
            
            if recent_posts:
                html = '<div style="margin-top: 25px; padding: 15px; background-color: #f9f9f9; border-left: 4px solid #007bff;">'
                html += '<h3>🔗 সম্পর্কিত আরও পোস্ট:</h3><ul>'
                for post in recent_posts:
                    title = post.get('title', 'অন্যান্য ব্লগ পোস্ট')
                    url = post.get('url')
                    html += f'<li><a href="{url}" target="_blank">{title}</a></li>'
                html += '</ul></div>'
                return html
    except Exception as e:
        print(f"Internal links format error: {e}")
    return ""

def generate_article(topic, category, keywords):
    """
    Gemini API ব্যবহার করে SEO ফ্রেন্ডলি বাংলা আর্টিকেল তৈরি করার ফাংশন (With Retry Mechanism)।
    """
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    keywords_str = ", ".join(keywords) if isinstance(keywords, list) else str(keywords)
    current_year = "2026"

    prompt = f"""
You are an expert SEO Tech Blogger for TechBangla.
Write a comprehensive, engaging, and fully SEO-optimized blog post in Bengali about: '{topic}'.
Category: {category}
Target Keywords: {keywords_str}

STRICT REQUIREMENTS:
1. Current Year is strictly {current_year}. NEVER use 2024 or 2025 anywhere in the title, headers, or body text.
2. Output ONLY clean HTML tags (<h2>, <h3>, <p>, <ul>, <li>, <b>, <table>, <tr>, <td>, <br/>). Do NOT use Markdown (no **, ###).
3. Do NOT invent or hardcode any internal links inside the content.
4. MUST include at least 3 high-authority external DOFOLLOW links (e.g., <a href="https://blog.google" target="_blank">Google Blog</a>, <a href="https://support.apple.com" target="_blank">Apple Support</a>). Do NOT use rel="nofollow".

Output Format MUST be exactly:

TITLE: [SEO Title in Bengali referencing {current_year}]

SEARCH_DESCRIPTION: [150 characters summary in Bengali]

LABELS: {category}, সাইবার নিরাপত্তা, টেক নিউজ

CONTENT:
[Introductory text in Bengali]

<h2>[Header 1 in Bengali]</h2>
[Details]

<h2>[Header 2 in Bengali]</h2>
[Details]

<h2>তুলনামূলক বিশ্লেষণ</h2>
<table border="1" style="width:100%; border-collapse: collapse; text-align: left; margin: 15px 0;">
  <tr style="background-color: #f2f2f2;">
    <th style="padding: 8px;">বিষয়</th>
    <th style="padding: 8px;">অপশন A</th>
    <th style="padding: 8px;">অপশন B</th>
  </tr>
  <tr>
    <td style="padding: 8px;">...</td>
    <td style="padding: 8px;">...</td>
    <td style="padding: 8px;">...</td>
  </tr>
</table>

<h2>উপসংহার</h2>
[Conclusion text in Bengali]

<!--INTERNAL_LINKS-->
"""

    # Automatic Function Calling (AFC) সংক্রান্ত ওয়ার্নিং দূর করতে খালি কনফিগারেশন পাস করা
    config = types.GenerateContentConfig(
        tools=[]
    )

    models_to_try = ['gemini-3.6-flash', 'gemini-2.5-flash']

    for model_name in models_to_try:
        for attempt in range(3):
            try:
                print(f"🔄 Requesting Gemini ({model_name}) - Attempt {attempt + 1}...")
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=config
                )
                
                raw_article = response.text
                
                # ইন্টারনাল লিঙ্ক যুক্ত করা
                internal_links_html = get_recent_internal_links()
                if "<!--INTERNAL_LINKS-->" in raw_article:
                    raw_article = raw_article.replace("<!--INTERNAL_LINKS-->", internal_links_html)
                else:
                    raw_article += f"\n\n{internal_links_html}"
                    
                return raw_article

            except Exception as e:
                print(f"⚠️ Attempt {attempt + 1} with {model_name} failed: {e}")
                if attempt < 2:
                    time.sleep(5)  # ৫ সেকেন্ড অপেক্ষা করে আবার চেষ্টা করবে

    raise Exception("❌ All Gemini API attempts failed due to server capacity limits.")
