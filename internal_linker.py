import os
import json
import random

def get_saved_posts():
    """blog_posts.json ফাইল থেকে আগের পোস্টের ডেটা পড়ার ফাংশন"""
    json_file = "blog_posts.json"
    if os.path.exists(json_file):
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def add_internal_links(content, category):
    posts = get_saved_posts()
    
    # ক্যাটাগরি অনুযায়ী ফিল্টার করা
    cat_posts = [p for p in posts if p.get("category") == category and p.get("url")]
    
    # ক্যাটাগরিতে পোস্ট না থাকলে সাধারণ পোস্ট থেকে নেওয়া
    if not cat_posts:
        cat_posts = [p for p in posts if p.get("url")]
        
    if not cat_posts:
        return content

    # ১. কন্টেন্টের মাঝামাঝি জায়গায় ১টি 'ইন-লাইন' ইন্টারলিংক বক্স যোগ করা
    featured_post = random.choice(cat_posts)
    inline_link_html = f'''
    <div style="background-color: #f0f7ff; border-left: 4px solid #0073aa; padding: 12px; margin: 20px 0; border-radius: 4px;">
        <strong>📌 এটিও পড়ুন:</strong> <a href="{featured_post['url']}" style="color: #0073aa; font-weight: bold; text-decoration: none;">{featured_post['title']}</a>
    </div>
    '''

    # কন্টেন্ট ভেঙে দ্বিতীয় প্যারাগ্রাফের পর ইন-লাইন লিংক বসানো
    paragraphs = content.split("</p>")
    if len(paragraphs) > 2:
        paragraphs.insert(2, inline_link_html)
        content = "</p>".join(paragraphs)
    else:
        content += inline_link_html

    # ২. কন্টেন্টের শেষে ৩টি পোস্টের একটি পরিষ্কার তালিকায় লিংক দেওয়া
    related_posts = cat_posts[:3]
    if related_posts:
        bottom_links = '<br/><h3>🔗 সম্পর্কিত আরও পোস্ট:</h3><ul>'
        for post in related_posts:
            bottom_links += f'<li><a href="{post["url"]}" target="_blank">{post["title"]}</a></li>'
        bottom_links += '</ul>'
        content += bottom_links

    return content
