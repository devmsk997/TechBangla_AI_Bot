import os
import json
import random

def get_saved_posts():
    """blog_posts.json ফাইল থেকে আগের পোস্টের ডেটা পড়ার ফাংশন"""
    json_file = "blog_posts.json"
    if os.path.exists(json_file):
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def add_internal_links(content, category, current_title=None):
    posts = get_saved_posts()
    
    #১. ফিল্টারিং: বর্তমান পোস্ট বাদ দেওয়া এবং সঠিক ইউআরএল নিশ্চিত করা
    valid_posts = [
        p for p in posts 
        if p.get("url") and p.get("title") and p.get("title") != current_title
    ]
    
    if not valid_posts:
        return content

    # ক্যাটাগরি অনুযায়ী ফিল্টার করা (Topic Cluster)
    cat_posts = [p for p in valid_posts if p.get("category") == category]
    
    # ক্যাটাগরিতে পোস্ট না থাকলে সাধারণ বৈধ পোস্ট ব্যবহার করা
    if not cat_posts:
        cat_posts = valid_posts

    # ২. ইন-লাইন ইন্টারলিংক তৈরি
    featured_post = random.choice(cat_posts)
    inline_link_html = f'''
    <div style="background-color: #f0f7ff; border-left: 4px solid #0073aa; padding: 12px; margin: 20px 0; border-radius: 4px;">
        <strong>📌 এটিও পড়ুন:</strong> <a href="{featured_post['url']}" target="_blank" style="color: #0073aa; font-weight: bold; text-decoration: none;">{featured_post['title']}</a>
    </div>
    '''

    # কন্টেন্টের ভেতরের উপযুক্ত স্থানে ইন-লাইন লিংক বসানো (নিরাপদ উপায়)
    if "</h2>" in content:
        # ১ম H2 ট্যাগের ঠিক আগে ইন-লাইন বক্স বসাবে
        parts = content.split("</h2>", 1)
        content = parts[0] + "</h2>" + inline_link_html + parts[1]
    elif "</p>" in content:
        paragraphs = content.split("</p>")
        if len(paragraphs) > 2:
            paragraphs.insert(2, inline_link_html)
            content = "</p>".join(paragraphs)
        else:
            content += inline_link_html
    else:
        content += inline_link_html

    # ৩. শেষের তালিকায় ইন-লাইন পোস্টটি বাদ দিয়ে ইউনিক ৩টি লিংক রাখা
    remaining_posts = [p for p in cat_posts if p['url'] != featured_post['url']]
    
    # ক্যাটাগরিতে আর পোস্ট না থাকলে বাকি যেকোনো পোস্ট থেকে ব্যাকআপ
    if len(remaining_posts) < 3:
        backup = [p for p in valid_posts if p['url'] != featured_post['url'] and p not in remaining_posts]
        remaining_posts.extend(backup)

    related_posts = remaining_posts[:3]

    if related_posts:
        bottom_links = '\n<br/><h2>🔗 সম্পর্কিত আরও পোস্ট:</h2>\n<ul>\n'
        for post in related_posts:
            bottom_links += f'  <li><a href="{post["url"]}" target="_blank">{post["title"]}</a></li>\n'
        bottom_links += '</ul>\n'
        content += bottom_links

    return content
