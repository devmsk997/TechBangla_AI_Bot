import json
import os
from datetime import datetime

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
    posts = load_posts()
    valid_posts = [p for p in posts if p.get("title") and p.get("url")]
    
    # টপিক ক্লাস্টার: একই ক্যাটাগরির লাইভ পোস্ট
    related = [p for p in valid_posts if p.get("category") == category]
    
    if len(related) < limit:
        others = [p for p in valid_posts if p not in related]
        related.extend(others)
        
    return related[:limit]

def create_internal_link_html(category):
    """
    পাইথন নিজে নিশ্চিতভাবে 404-মুক্ত আসল ইন্টারলিংক তৈরি করবে
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
    current_year = "2026"  # বর্তমান সাল ফিক্সড

    prompt = f"""
You are an expert SEO Tech Blogger for TechBangla.
Write a comprehensive, engaging, and fully SEO-optimized blog post in Bengali about: '{topic}'.
Category: {category}
CRITICAL TIME REQUIREMENT: Current Year is strictly {current_year}. Do NOT write 2024 or 2025 anywhere in titles or content. Always use {current_year}.

STRICT FORMATTING RULES:
1. Do NOT use Markdown syntax (no **, ###). Use pure HTML tags (<h2>, <ul>, <li>, <b>, <table>, <tr>, <td>, <br/>).
2. Do NOT write any internal links inside the content body yourself. (Internal links will be appended safely by Python to prevent 404 errors).
3. Output template structure MUST be:

TITLE: [SEO Title in Bengali referencing {current_year}]

SEARCH_DESCRIPTION: [150 chars summary referencing {current_year}]

LABELS: {category}, সাইবার নিরাপত্তা, টেক নিউজ

CONTENT:
[Introductory text in Bengali]

<h2>[Header 1 in Bengali]</h2>
[Details]

<h2>[Header 2 in Bengali]</h2>
[Details]

[MUST INCLUDE AT LEAST 3 HIGH AUTHORITY EXTERNAL DOFOLLOW LINKS (e.g. <a href="https://blog.google" target="_blank">Google Blog</a>, <a href="https://support.apple.com" target="_blank">Apple Support</a>). NEVER USE rel="nofollow"]

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
