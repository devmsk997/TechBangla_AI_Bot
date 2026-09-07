import random
import re

KEYWORD_DATABASE = {
    "সাইবার নিরাপত্তা": [
        "cyber security tips 2026",
        "online security guidelines",
        "strong password protection",
        "phishing attack protection",
        "data privacy and safety",
        "ransomware protection",
        "vpn security tips"
    ],

    "AI টুলস": [
        "best AI tools 2026",
        "AI productivity tools",
        "AI automation for workflow",
        "latest AI technology",
        "generative AI tools",
        "chatgpt alternative tools"
    ],

    "মোবাইল টিপস": [
        "android tips and tricks",
        "smartphone performance optimization",
        "mobile battery save tips",
        "smartphone security guide",
        "android hidden features"
    ],

    "অ্যাপস": [
        "best android apps 2026",
        "useful mobile applications",
        "app privacy and security",
        "must have productivity apps"
    ],

    "টেক নিউজ": [
        "latest technology news 2026",
        "tech updates bangla",
        "AI news updates",
        "Google latest algorithm updates",
        "cyber crime tech news"
    ]
}


def research_keywords(category, topic):
    """
    ক্যাটাগরি ও টপিক অনুযায়ী প্রাইমারি ও সেকেন্ডারি কিওয়ার্ড জেনারেট করে
    """
    # ১. ক্যাটাগরি অনুযায়ী কিওয়ার্ড সিলেক্ট করা
    keywords = KEYWORD_DATABASE.get(category, [
        "latest technology trends", 
        "tech news bangla", 
        "digital security guide"
    ])

    primary = topic.strip().lower()

    # ২. টপিক থেকেও ২/১টি কিওয়ার্ড অটো-এক্সট্র্যাক্ট করা
    extracted_terms = [w for w in re.findall(r'\w+', primary) if len(w) > 3]

    # ৩. ডাটাবেস থেকে র্যান্ডম কিওয়ার্ড নেওয়া
    sample_count = min(3, len(keywords))
    related = random.sample(keywords, sample_count)

    # ৪. টপিক থেকে এক্সট্র্যাক্ট করা শব্দ কিওয়ার্ডে যোগ করা (যদি থাকে)
    if extracted_terms:
        related.append(f"{extracted_terms[0]} guide")

    return {
        "primary_keyword": primary,
        "related_keywords": list(set(related))  # ডুপ্লিকেট রিমুভ করা
    }
