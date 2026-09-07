import json
import os

POSTS_FILE = "blog_posts.json"

def load_posts():
    if os.path.exists(POSTS_FILE):
        try:
            with open(POSTS_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception:
            return []
    return []

def save_post(title, url, category):
    posts = load_posts()

    # টাইটেল বা ইউআরএল না থাকলে সেভ হবে না
    if not title or not url:
        return

    # ডুप्लिकেট ইউআরএল এড়াতে
    for post in posts:
        if post.get("url") == url:
            return

    posts.append({
        "title": title,
        "url": url,
        "category": category
    })

    with open(POSTS_FILE, "w", encoding="utf-8") as file:
        json.dump(posts, file, ensure_ascii=False, indent=4)

def get_related_posts(category, limit=5):
    """
    ক্যাটাগরি অনুযায়ী সম্পর্কিত পোস্ট আনবে, 
    না পাওয়া গেলে অন্য ক্যাটাগরির লাইভ পোস্ট ব্যাকআপ হিসেবে দেবে।
    """
    posts = load_posts()
    valid_posts = [p for p in posts if p.get("title") and p.get("url")]
    
    # সমজাতীয় ক্যাটাগরির পোস্ট
    related = [p for p in valid_posts if p.get("category") == category]
    
    # একই ক্যাটাগরিতে পোস্ট কম থাকলে অন্যান্য পোস্ট যুক্ত করবে
    if len(related) < limit:
        others = [p for p in valid_posts if p not in related]
        related.extend(others)
        
    return related[:limit]

def generate_blog_prompt(topic, category):
    """
    AI-কে পারফেক্ট এইচটিএমএল, ৩টি External Link এবং 
    json ফাইলের সঠিক ইউআরএল দিয়ে পোস্ট তৈরি করার প্রম্পট।
    """
    related_posts = get_related_posts(category, limit=6)
    
    # AI-এর জন্য ব্যাকআপ হিসেবে সঠিক ইন্টারলিংক লিংক তৈরি
    internal_links_context = json.dumps(related_posts, ensure_ascii=False)

    prompt = f"""
You are an expert SEO Tech Blogger for TechBangla.
Write a comprehensive, engaging, and fully SEO-optimized blog post in Bengali about: '{topic}'.
Category: {category}

STRICT FORMATTING & OUTPUT RULES:
1. Do NOT use Markdown syntax (no **, ###, etc.). Use HTML tags exclusively (<h2>, <ul>, <li>, <b>, <table>, <tr>, <td>, <br/>).
2. Use the exact template structure below:

TITLE: [SEO Friendly Title in Bengali]

SEARCH_DESCRIPTION: [150-160 characters summary in Bengali]

LABELS: {category}, সাইবার নিরাপত্তা, টেক নিউজ

CONTENT:
[Introductory paragraphs]

<div class="separator" style="clear: both; text-align: center; margin-bottom: 25px;">
    <a href="FEATURED_IMAGE_URL" style="margin-left: 1em; margin-right: 1em;">
        <img border="0" data-original-height="675" data-original-width="1200" src="FEATURED_IMAGE_URL" alt="{topic}" title="{topic}" loading="eager" width="1200" height="675" style="max-width:100%; height:auto; border-radius:8px;" />
    </a>
</div>

📌 এটিও পড়ুন: <a href="SELECT_ONE_EXACT_URL_FROM_JSON" target="_blank">SELECT_MATCHING_TITLE_FROM_JSON</a>

<h2>[Section Header 1 in Bengali]</h2>
[Detailed content]

<h2>[Section Header 2 in Bengali]</h2>
[Detailed content]

[MUST INCLUDE AT LEAST 3 HIGH AUTHORITY EXTERNAL LINKS WITH rel="nofollow" target="_blank" TO OFFICIAL SOURCES (e.g., Google Support, Microsoft, FIDO Alliance, Wikipedia, or official product documentation)]

<h2>তুলনামূলক বিশ্লেষণ (Comparison Table)</h2>
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
[Conclusion paragraph]

🔗 **সম্পর্কিত আরও পোস্ট:**
<ul>
  <li><a href="EXACT_URL_1" target="_blank">EXACT_TITLE_1</a></li>
  <li><a href="EXACT_URL_2" target="_blank">EXACT_TITLE_2</a></li>
  <li><a href="EXACT_URL_3" target="_blank">EXACT_TITLE_3</a></li>
</ul>

CRITICAL LINKING INSTRUCTION:
- You MUST only use the exact URLs provided in this JSON list for internal links:
{internal_links_context}
- NEVER invent or guess an internal URL. Incorrect URLs cause 404 errors.
"""
    return prompt
