import os
import requests
import urllib.parse
import random
from github_image import upload_image

def get_style(title):
    title_lower = title.lower()

    if any(word in title_lower for word in ["ransomware", "malware", "phishing", "security", "password", "vpn", "data breach", "cyber"]):
        return "Cybersecurity wallpaper, dark digital background, glowing glowing encrypted network, blue and red neon lighting, cinematic 3D tech style"

    elif any(word in title_lower for word in ["ai", "artificial intelligence", "chatgpt", "machine learning", "gemini"]):
        return "Futuristic artificial intelligence background, glowing neural network, cyan holographic interface, hyperrealistic 3D render"

    elif any(word in title_lower for word in ["phone", "smartphone", "android", "mobile"]):
        return "High-end flagship smartphone concept, sleek glossy design, vibrant futuristic display, professional studio product lighting"

    elif any(word in title_lower for word in ["app", "application", "software"]):
        return "Modern UI UX design concept, sleek glassmorphism app interface, floating digital screens, clean modern aesthetic"

    else:
        return "Ultra modern technology presentation, abstract digital network, clean minimal premium tech background, 8k resolution"


def generate_image(title):
    style = get_style(title)
    
    # HD & High Quality Pollinations Prompt Injection
    prompt = f"Unreal Engine 5 render, highly detailed, crisp focus, 8k resolution, cinematic lighting, 16:9 aspect ratio, professional blog cover photo of {title}, style of {style}, no text, no watermark, no logo, photorealistic"
    encoded_prompt = urllib.parse.quote(prompt)
    seed = random.randint(1000, 999999)

    # Flux model enhancement + Enhance parameter for sharp quality
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

        print("⚠️ Pollinations or upload failed, using dynamic Fallback URL.")
        return url

    except Exception as e:
        print("⚠️ Image generation error:", e)
        # ৪. ব্যাকআপ টেকনোলজি ছবি (Unsplash HD)
        return "https://images.unsplash.com/photo-1518770660439-4636190af475?w=1280&auto=format&fit=crop"
