import os
import requests
import urllib.parse
import random
from github_image import upload_image

def get_style(title):
    title_lower = title.lower()

    if any(word in title_lower for word in ["ransomware", "malware", "phishing", "security", "password", "vpn", "data breach", "cyber"]):
        return "Cybersecurity theme, dark digital environment, encrypted data, security lock, network protection, hacker threat visualization, blue and red neon lighting, realistic 3D technology style"

    elif any(word in title_lower for word in ["ai", "artificial intelligence", "chatgpt", "machine learning"]):
        return "Artificial intelligence theme, futuristic AI brain, neural network, digital hologram, advanced technology interface, blue futuristic lighting, realistic 3D render style"

    elif any(word in title_lower for word in ["phone", "smartphone", "android", "mobile"]):
        return "Modern smartphone technology, premium mobile device, digital interface, performance optimization concept, clean futuristic background, realistic product photography style"

    elif any(word in title_lower for word in ["app", "application"]):
        return "Mobile application technology, modern app interface, smartphone screen, digital ecosystem, clean professional technology design, realistic 3D style"

    else:
        return "Modern technology concept, digital world, future technology, computer interface, clean premium tech magazine style, realistic 3D render"


def generate_image(title):
    style = get_style(title)
    
    # Pollinations AI Prompt
    prompt = f"Professional technology blog featured image. Topic: {title}. Style: {style}. Requirements: Premium technology magazine quality, realistic 3D render, high detail, 16:9 aspect ratio, no text, no logo."
    encoded_prompt = urllib.parse.quote(prompt)
    seed = random.randint(1000, 999999)

    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&width=1280&height=720&nologo=true"
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

        print("⚠️ Pollinations or upload failed, using dynamic Fallback URL.")
        # ৩. কোনো কারণে এপিআই ফেল করলে নিরাপদ ডাইনামিক ইউআরএল রিটার্ন
        return url

    except Exception as e:
        print("⚠️ Image generation error:", e)
        # ৪. এক্সেপশন হলে ব্যাকআপ আনস্প্ল্যাশ টেকনোলজি ছবি
        return "https://images.unsplash.com/photo-1518770660439-4636190af475?w=1280&auto=format&fit=crop"
