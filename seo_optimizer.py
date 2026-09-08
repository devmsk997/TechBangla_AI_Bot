import re

def clean_html(raw_html):
    """HTML ট্যাগ ও অতিরিক্ত স্পেস মুছে পরিষ্কার বাংলা টেক্সট বের করার ফাংশন"""
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, ' ', raw_html)
    return re.sub(r'\s+', ' ', cleantext).strip()

def optimize_seo(title, content, category):
    # ১. টাইটেল ও কন্টেন্ট ক্লিন করা
    clean_title = re.sub(r'\s+', ' ', title).strip()
    plain_content = clean_html(content)

    # ২. কন্টেন্টের প্রথম ১৫০-১৬০ অক্ষর থেকে ডাইনামিক সার্চ ডেসক্রিপশন তৈরি
    if len(plain_content) > 150:
        search_description = plain_content[:155].strip() + "..."
    else:
        search_description = f"{clean_title} সম্পর্কে বিস্তারিত জানুন TechBangla-তে। সঠিক তথ্য ও গাইডলাইন।"

    # ৩. আসল বাংলা শব্দের সংখ্যা গণনা
    word_count = len(plain_content.split())

    # ৪. ডাইনামিক প্রাইমারি ও সেকেন্ডারি কিওয়ার্ড
    primary_keyword = clean_title.lower()
    keywords = [
        clean_title,
        category,
        f"{category} ২০২৬",
        "বাংলা টেক গাইড",
        "TechBangla"
    ]

    # ৫. কেস-ইনসেনসিটিভ উপায়ে H2 এবং H3 ট্যাগ চেক
    has_h2 = bool(re.search(r'<h2', content, re.IGNORECASE))
    has_h3 = bool(re.search(r'<h3', content, re.IGNORECASE))

    # SEO রিপোর্ট রিটার্ন
    seo_data = {
        "primary_keyword": primary_keyword,
        "keywords": keywords,
        "search_description": search_description,
        "word_count": word_count,
        "seo_check": {
            "title_length": len(clean_title),
            "content_word_count": word_count,
            "has_h2": has_h2,
            "has_h3": has_h3,
            "is_seo_friendly": has_h2 and word_count >= 500
        }
    }

    return seo_data
