import os
import requests
import urllib.parse
import random
import re
from github_image import upload_image

def get_style(title):
    title_lower = title.lower()

    # ১. সাইবার নিরাপত্তা (Cybersecurity)
    if any(word in title_lower for word in ["cyber", "security", "password", "vpn", "malware", "phishing", "নিরাপত্তা", "পাসওয়ার্ড", "হ্যাক", "স্ক্যাম"]):
        return "Cybersecurity wallpaper, dark digital network background, glowing encrypted data, neon lighting, 3D tech style"

    # ২. কৃত্রিম বুদ্ধিমত্তা (AI Tools)
    elif any(word in title_lower for word in ["ai", "chatgpt", "gemini", "intelligence", "এআই", "বুদ্ধিমত্তা", "চ্যাটজিপিটি"]):
        return "Futuristic artificial intelligence background, glowing neural network, cyan holographic interface, hyperrealistic 3D render"

    # ৩. স্মার্টফোন ও মোবাইল (Smartphone & Mobile)
    elif any(word in title_lower for word in ["phone", "smartphone", "android", "mobile", "স্মার্টফোন", "ফোন", "মোবাইল", "অ্যান্ড্রয়েড", "স্পিড", "ধীরগতি"]):
        return "High-end modern smartphone concept, glossy metallic back, vibrant futuristic display, professional tech studio lighting"

    # ৪. অ্যাপস ও সফটওয়্যার (Apps)
    elif any(word in title_lower for word in ["app", "software", "অ্যাপ", "সফটওয়্যার"]):
        return "Modern UI UX design concept, sleek glassmorphism app interface, floating digital screens, clean aesthetic"

    # ৫. ডিফল্ট টেকনোলজি (Default Fallback)
    else:
        return "Ultra modern technology presentation, abstract digital network, clean premium tech background"


def generate_image(title):
    style = get_style(title)
    
    # টাইটেল থেকে স্পেশাল ক্যারেক্টার বাদ দিয়ে শুধু ইংরেজি কিওয়ার্ড বের করা (প্রম্পটের সেফটির জন্য)
    clean_prompt_subject = re.sub(r'[^a-zA-Z0-9\s]', '', title).strip()
    if not clean_prompt_subject:
        clean_prompt_subject = "modern technology topic"

    # HD & High Quality Pollinations Prompt Injection
    prompt = f"Unreal Engine 5 render, highly detailed, crisp focus, 8k resolution, cinematic lighting, 16:9 aspect ratio, professional blog cover photo representing {clean_prompt_subject}, {style}, no text, no watermark, no logo, photorealistic"
    encoded_prompt = urllib.parse.quote(prompt)
    seed = random.randint(1000, 999999)

    # Flux model enhancement
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&width=1280&height=720&model=flux&enhance=true&nologo=true"
    filename = "featured_image.jpg"

    try:
        # ১. Pollinations থেকে ছবি ডাউনলোড
        response = requests.get(url, timeout=45)
        if response.status_code == 200:
            with open(filename, "wb") as file:
                file.write(response.content)
            print("📸 Image downloaded locally successfully:", filename)

            # ২. ডাউনলোড করা ছবি GitHub CDN-এ আপলোড
            uploaded_url = upload_image(filename)
            if uploaded_url:
                return uploaded_url

        print("⚠️ Pollinations or upload failed, using dynamic Direct Pollinations URL.")
        return url

    except Exception as e:
        print("⚠️ Image generation error:", e)
        # ৩. ব্যাকআপ টেকনোলজি ছবি (Unsplash HD)
        return "https://images.unsplash.com/photo-1518770660439-4636190af475?w=1280&auto=format&fit=crop"
