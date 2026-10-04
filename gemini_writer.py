import os
import json
import time
from google import genai
from google.genai import types

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def get_available_posts_for_linking():
    """
    blog_posts.json থেকে সব পোস্টের টাইটেল ও লিংক রিটার্ন করে, 
    যাতে এআই সেগুলোর মধ্যে থেকে প্রাসঙ্গিক অ্যাঙ্কর টেক্সট লিংক তৈরি করতে পারে।
    """
    try:
        if os.path.exists('blog_posts.json'):
            with open('blog_posts.json', 'r', encoding='utf-8') as f:
                posts = json.load(f)
            
            # শুধুমাত্র বৈধ URL আছে এমন পোস্টগুলো ফিল্টার করা
            valid_posts = [p for p in posts if isinstance(p, dict) and p.get('url') and p.get('title')]
            return valid_posts[-10:] # সাম্প্রতিক ১০টি পোস্ট পাঠাতে পারেন
    except Exception as e:
        print(f"Error loading posts for internal linking: {e}")
    return []

def generate_article(topic, category, keywords):
    """
    Gemini API ব্যবহার করে SEO ফ্রেন্ডলি বাংলা আর্টিকেল তৈরি করার ফাংশন (Contextual Internal Linking সহ)।
    """
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    keywords_str = ", ".join(keywords) if isinstance(keywords, list) else str(keywords)
    current_year = "2026"

    # আগের পোস্টগুলোর লিস্ট সংগ্রহ করা
    existing_posts = get_available_posts_for_linking()
    linking_instructions = ""
    
    if existing_posts:
        linking_instructions = "Available posts for Contextual Internal Linking (Use these exact URLs as anchor text naturally inside the body text where relevant):\n"
        for post in existing_posts:
            linking_instructions += f"- Title: '{post.get('title')}' | URL: {post.get('url')}\n"
    else:
        linking_instructions = "No previous posts available for internal linking yet."

    prompt = f"""
You are an expert SEO Tech Blogger for TechBangla.
Write a comprehensive, engaging, highly detailed, and fully SEO-optimized long-form blog post in Bengali about: '{topic}'.
Category: {category}
Target Keywords: {keywords_str}

{linking_instructions}

STRICT REQUIREMENTS:
1. Current Year is strictly {current_year}. NEVER use 2024 or 2025 anywhere in the title, headers, or body text.
2. TITLE LENGTH: The SEO Title in Bengali MUST be strictly within 60 characters (max 60 characters). Keep it concise and attractive.
3. ARTICLE LENGTH: Write an extensive, deep-dive article containing at least 2000 words. Expand all sections thoroughly with detailed explanations, steps, and examples.
4. CONTEXTUAL INTERNAL LINKING: Naturally weave at least 2 to 3 internal links from the "Available posts" list above into the body paragraphs using meaningful anchor texts in Bengali. Format as HTML: <a href="URL">Anchor Text</a>. Do NOT put them all at the end; integrate them smoothly into sentences.
5. Output ONLY clean HTML tags (<h2>, <h3>, <p>, <ul>, <li>, <b>, <table>, <tr>, <td>, <br/>). Do NOT use Markdown (no **, ###).
6. MUST include at least 3 high-authority external DOFOLLOW links (e.g., <a href="https://blog.google" target="_blank">Google Blog</a>, <a href="https://support.apple.com" target="_blank">Apple Support</a>). Do NOT use rel="nofollow".

Output Format MUST be exactly:

TITLE: [SEO Title in Bengali referencing {current_year} and strictly under 60 characters]

SEARCH_DESCRIPTION: [150 characters summary in Bengali]

LABELS: {category}, সাইবার নিরাপত্তা, টেক নিউজ

CONTENT:
[Introductory text in Bengali with natural internal links]

<h2>[Header 1 in Bengali]</h2>
[Detailed content with multiple paragraphs and sub-sections]

<h2>[Header 2 in Bengali]</h2>
[Detailed content with multiple paragraphs and sub-sections]

<h2>[Header 3 in Bengali]</h2>
[Detailed content with multiple paragraphs and sub-sections]

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
"""

    # Automatic Function Calling (AFC) সংক্রান্ত ওয়ার্নিং দূর করতে খালি কনফিগারেশন পাস করা
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
                return raw_article

            except Exception as e:
                print(f"⚠️ Attempt {attempt + 1} with {model_name} failed: {e}")
                if attempt < 2:
                    time.sleep(5)  # ৫ সেকেন্ড অপেক্ষা করে আবার চেষ্টা করবে

    raise Exception("❌ All Gemini API attempts failed due to server capacity limits.")
