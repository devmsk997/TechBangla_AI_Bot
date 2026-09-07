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

    if not title or not url:
        return

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

def get_related_posts(category, limit=4):
    """
    একই ক্যাটাগরির পোস্ট এনে টপিক ক্লাস্টার তৈরি করে। 
    কম থাকলে অন্য ক্যাটাগরির আসল পোস্ট ব্যাকআপ হিসেবে দেবে।
    """
    posts = load_posts()
    valid_posts = [p for p in posts if p.get("title") and p.get("url")]
    
    # একই ক্যাটাগরির সঠিক পোস্ট (Topic Cluster)
    related = [p for p in valid_posts if p.get("category") == category]
    
    if len(related) < limit:
        others = [p for p in valid_posts if p not in related]
        related.extend(others)
        
    return related[:limit]

def create_internal_link_html(category):
    """
    পাইথন নিজে নিশ্চিতভাবে ১০০% সঠিক HTML লিংক তৈরি করবে, যা ৪-০-৪ হবে না।
    """
    related = get_related_posts(category, limit=4)
    if not related:
        return ""

    html = "\n\n<h2>🔗 সম্পর্কিত আরও পোস্ট:</h2>\n<ul>\n"
    for post in related:
        html += f'  <li><a href="{post["url"]}" target="_blank">{post["title"]}</a></li>\n'
    html += "</ul>\n"
    
    return html

def generate_blog_prompt(topic, category):
    prompt = f"""
You are an expert SEO Tech Blogger for TechBangla.
Write a comprehensive, engaging, and fully SEO-optimized blog post in Bengali about: '{topic}'.
Category: {category}

STRICT FORMATTING Rules:
1. Do NOT use Markdown syntax (no **, ###). Use pure HTML tags (<h2>, <ul>, <li>, <b>, <table>, <tr>, <td>, <br/>).
2. Output template structure MUST be:

TITLE: [SEO Title in Bengali]

SEARCH_DESCRIPTION: [Summary 150 chars]

LABELS: {category}, সাইবার নিরাপত্তা, টেক নিউজ

CONTENT:
[Introductory text]

<h2>[Header 1]</h2>
[Details]

<h2>[Header 2]</h2>
[Details]

[MUST INCLUDE AT LEAST 3 DOFOLLOW EXTERNAL LINKS TO OFFICIAL SITES e.g. <a href="https://blog.google" target="_blank">Google Blog</a>, <a href="https://support.microsoft.com" target="_blank">Microsoft Support</a>. DO NOT USE rel="nofollow"]

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
[Conclusion text]
"""
    return prompt
