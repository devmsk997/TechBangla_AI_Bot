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

def get_related_posts(category, limit=5):
    posts = load_posts()
    valid_posts = [p for p in posts if p.get("title") and p.get("url")]
    
    related = [p for p in valid_posts if p.get("category") == category]
    
    if len(related) < limit:
        others = [p for p in valid_posts if p not in related]
        related.extend(others)
        
    return related[:limit]

def generate_blog_prompt(topic, category):
    related_posts = get_related_posts(category, limit=6)
    internal_links_context = json.dumps(related_posts, ensure_ascii=False)

    prompt = f"""
You are an expert SEO Tech Blogger for TechBangla.
Write a comprehensive, engaging, and fully SEO-optimized blog post in Bengali about: '{topic}'.
Category: {category}

STRICT FORMATTING & OUTPUT RULES:
1. Do NOT use Markdown syntax (no **, ###, etc.). Use HTML tags exclusively (<h2>, <ul>, <li>, <b>, <table>, <tr>, <td>, <br/>).
2. Output Format MUST follow this template strictly:

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

📌 এটিও পড়ুন: <a href="EXACT_URL_FROM_JSON" target="_blank">EXACT_TITLE_FROM_JSON</a>

<h2>[Section Header 1 in Bengali]</h2>
[Detailed content]

<h2>[Section Header 2 in Bengali]</h2>
[Detailed content]

[MUST INCLUDE AT LEAST 3 HIGH AUTHORITY EXTERNAL DOFOLLOW LINKS (e.g. <a href="https://blog.google" target="_blank">Google Blog</a>). DO NOT USE rel="nofollow"]

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

CRITICAL LINKING INSTRUCTIONS:
- You MUST only use the exact URLs provided in this JSON list for internal links:
{internal_links_context}
- ALWAYS create proper HTML anchor tags (<a href="...">Title</a>) for both internal and external links. Never print raw text URLs without HTML.
"""
    return prompt
