import os
import requests
import base64

GITHUB_TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
GITHUB_REPO = "devmsk997/modern-kitchen-blog-images"

def upload_image(image_path):
    """
    Uploads a local image file to GitHub repository and returns the CDN/raw URL.
    If credentials or upload fails, it gracefully handles the exception.
    """
    if not image_path or not os.path.exists(image_path):
        print("⚠️ Image path invalid or file does not exist.")
        return None

    if not GITHUB_TOKEN:
        print("⚠️ GITHUB_TOKEN not found in environment. Skipping GitHub image upload.")
        return None

    try:
        filename = os.path.basename(image_path)
        with open(image_path, "rb") as file:
            content = base64.b64encode(file.read()).decode("utf-8")

        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/images/{filename}"
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        data = {
            "message": f"Upload image {filename}",
            "content": content
        }

        response = requests.put(url, headers=headers, json=data)
        if response.status_code in [200, 201]:
            raw_url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/images/{filename}"
            print(f"🖼️ Image uploaded successfully to GitHub: {raw_url}")
            return raw_url
        else:
            print(f"⚠️ Image upload failed: {response.json().get('message', 'Unknown error')}")
            return None
    except Exception as e:
        print(f"⚠️ Error during GitHub image upload: {e}")
        return None
