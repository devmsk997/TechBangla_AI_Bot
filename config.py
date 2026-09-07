import os

# GitHub Secrets / Environment Variables থেকে মান সংগ্রহ
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
BLOG_ID = os.environ.get("BLOG_ID")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
GITHUB_TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")

GITHUB_USERNAME = "devmsk997"
GITHUB_REPO = "techbangla-image-hosting" # আপনার ইমেজ রেপোজিটরি নাম
