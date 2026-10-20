import os
import json
import time
from google import genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def get_available_posts_for_linking():
    """
    blog_posts.json থেকে সাম্প্রতিক পোস্টগুলোর টাইটেল ও ইউআরএল সংগ্রহ করে,
    যাতে এআই লেখার ভেতরে প্রাসঙ্গিক অ্যাঙ্কর টেক্সট লিংক তৈরি করতে পারে।
    """
    try:
        if os.path.exists('blog_posts.json'):
            with open('blog_posts.json', 'r', encoding='utf-8') as f:
                posts = json.load(f)
            
            valid_posts = [p for p in posts if isinstance(p, dict) and p.get('url') and p.get('title')]
            return valid_posts[-10:] # সাম্প্রতিক ১০টি পোস্ট
    except Exception as e:
        print(f"Error loading posts for internal linking: {e}")
    return []

def generate_article(topic, category, keywords):
    """
    Gemini API ব্যবহার করে ৬০ অক্ষরের টাইটেল, ২০০০+ শব্দের আর্টিকেল এবং কন্টেকচুয়াল অ্যাঙ্কর টেক্সট লিংকিং সহ জেনারেট করার ফাংশন।
    """
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    keywords_str = ", ".join(keywords) if isinstance(keywords, list) else str(keywords)
    current_year = "2026"

    # blog_posts.json থেকে আগের পোস্টগুলোর লিস্ট নেওয়া
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
1. Current Year is strictly {current_year}. NEVER use 2024 or 2025 anywhere in the title, headers, or body text
2. TITLE LENGTH: The SEO Title in Bengali MUST be strictly within 60 characters (max 60 characters). Keep it concise and attractive.
3. ARTICLE LENGTH: Write an extensive, deep-dive article containing at least 2000 words. Expand all sections thoroughly with detailed explanations, steps, and examples.
4. CONTEXTUAL INTERNAL LINKING: Naturally weave at least 2 to 3 internal links from the "Available posts" list above into the body paragraphs using meaningful anchor texts in Bengali. Format as HTML: <a href="URL">Anchor Text</a>. Do NOT put them in a footer box; integrate them smoothly into sentences.
5. Output ONLY clean HTML tags (<h2>, <h3>, <p>, <ul>, <li>, <b>, <table>, <tr>, <td>, <br/>). Do NOT use Markdown (no **, ###).
6. MUST include at least 3 high-authority external DOFOLLOW links (e.g., <a href="https://blog.google" target="_blank">Google Blog</a>, <a href="https://support.apple.com" target="_blank">Apple Support</a>). Do NOT use rel="nofollow".

Output Format MUST be exactly:

TITLE: [SEO Title in Bengali referencing {current_year} and strictly under 60 characters]

SEARCH_DESCRIPTION: [150 characters summary in Bengali]

LABELS: [Generate 3 to 4 comma-separated tags based on category '{category}' and topic. Strictly format with a space after every comma e.g. "tag1, tag2, tag3". Do NOT add a trailing comma at the end.]

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

    # সচল ও ফ্রি মডেল লিস্ট আপডেট (গুগল অফিসিয়াল সাপোর্ট অনুযায়ী)
    models_to_try = [
        'gemini-3.8-flash',
        'gemini-2.5-flash-lite',
        'gemini-1.5-flash',
        'gemini-1.5-pro'
    ]

    max_retries_per_model = 3

    for model_name in models_to_try:
        for attempt in range(max_retries_per_model):
            try:
                print(f"🔄 Requesting Free Model ({model_name}) - Attempt {attempt + 1}...")
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                
                raw_article = response.text
                if raw_article:
                    print(f"✅ Successfully generated article using model: {model_name}")
                    return raw_article

            except Exception as e:
                err_str = str(e)
                print(f"⚠️ Model {model_name} failed on attempt {attempt + 1} due to: {err_str}")
                
                # ৫০৩ (Server Busy / High Demand) আসলে কিছুটা সময় বিরতি দিয়ে আবার চেষ্টা করবে
                if "503" in err_str or "UNAVAILABLE" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                    wait_time = (attempt + 1) * 10  # ১০ সেকেন্ড, ২০ সেকেন্ড, ৩০ সেকেন্ড ওয়েট করবে
                    print(f"⏳ Server is busy. Waiting {wait_time} seconds before retrying...")
                    time.sleep(wait_time)
                else:
                    # ৪০৪ (মডেল না পাওয়া গেলে) সরাসরি পরের মডেলে চলে যাবে
                    break
        
        print(f"🔄 Moving to the next active free model in sequence...")

    raise Exception("❌ All Free Gemini API models failed sequentially due to high demand or capacity limits.")
