import json
import os
import random

POST_FILE = "posted_topics.json"

TOPIC_CLUSTERS = {
    "সাইবার নিরাপত্তা": [
        "Password Security & Passkeys",
        "Phishing & Spear Phishing",
        "OTP Scam & SIM Swapping",
        "2FA & Multi-Factor Auth",
        "Malware & Spyware Protection",
        "Ransomware Attack Trends 2026",
        "VPN & Public Wi-Fi Safety",
        "Deepfake Fraud Detection",
        "Password Manager Comparison",
        "Data Breach Protection",
        "Social Engineering Awareness"
    ],

    "AI টুলস": [
        "ChatGPT & GPT-5 Features",
        "Best AI Tools 2026",
        "AI Productivity Hacks",
        "AI Image & Video Generator",
        "AI Security & Privacy Risks",
        "Claude & Gemini AI Comparison",
        "AI Code Assistants"
    ],

    "গ্যাজেট রিভিউ": [
        "Lenovo LP40 TWS Wireless Earbuds Review",
        "Smart Watch T800 Ultra Features and Price",
        "Kemei Electric Trimmer Complete Review",
        "Baseus Fast Charging Power Bank Review",
        "Solar PTZ 4G Security Camera Review",
        "Dahua CC Camera Setup and Price in BD"
    ],

    "মোবাইল টিপস": [
        "Android Optimization & Battery Saver",
        "Phone Performance Speedup",
        "Smartphone Security & Malware",
        "Android Hidden Developer Settings",
        "Mobile Data Savings Tips"
    ],

    "অ্যাপস": [
        "Must Have Android Apps 2026",
        "Useful Productivity Apps",
        "App Security & Permissions Guide",
        "Open Source Android Apps"
    ],

    "টেক নিউজ": [
        "AI Technology Updates 2026",
        "Google Algorithm & SEO News",
        "Cyber Crime Tech News",
        "Tech Innovations in Bangladesh"
    ]
}


def load_previous():
    """পূর্বে ব্যবহৃত টপিকগুলো লোড করা"""
    if os.path.exists(POST_FILE):
        try:
            with open(POST_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception:
            return []
    return []


def save_topic(topic):
    """ব্লগে সফল পোস্ট হওয়ার পর টপিকটি লিস্টে সেভ রাখা"""
    old = load_previous()
    if topic not in old:
        old.append(topic)

    with open(POST_FILE, "w", encoding="utf-8") as file:
        json.dump(old, file, ensure_ascii=False, indent=4)


def choose_topic():
    """নতুন টপিক সিলেক্ট করার মূল ফাংশন"""
    old_topics = load_previous()
    available = []

    for category, topics in TOPIC_CLUSTERS.items():
        for topic in topics:
            if topic not in old_topics:
                available.append((topic, category))

    # সব topic শেষ হলে ইতিহাস রিসেট করবে
    if not available:
        print("🔄 All topics covered. Resetting topic history...")
        with open(POST_FILE, "w", encoding="utf-8") as file:
            json.dump([], file)

        for category, topics in TOPIC_CLUSTERS.items():
            for topic in topics:
                available.append((topic, category))

    # র্যান্ডম একটি টপিক নির্বাচন
    selected_topic, selected_category = random.choice(available)

    return selected_topic, selected_category
