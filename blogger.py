from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

import os
import json
from datetime import datetime

from config import BLOG_ID
from blog_content import save_post

SCOPES = ["https://www.googleapis.com/auth/blogger"]

def get_service():
    creds = None
    
    # গিটহাব এনভায়রনমেন্ট ভ্যারিয়েবল (Secrets) থেকে টোকেন চেক করা
    token_json_env = os.environ.get("GOOGLE_TOKEN_JSON") or os.environ.get("TOKEN_JSON")
    credentials_json_env = os.environ.get("GOOGLE_CREDENTIALS_JSON") or os.environ.get("CREDENTIALS_JSON")

    if token_json_env:
        try:
            token_data = json.loads(token_json_env)
            creds = Credentials.from_authorized_user_info(token_data, SCOPES)
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
        except Exception as e:
            print(f"Error loading token from environment: {e}")

    # যদি এনভায়রনমেন্টে না থাকে, তবে লোকাল token.json চেক করবে (লোকাল পিসির জন্য)
    if not creds and os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # যদি টোকেন ভ্যালিড না হয় এবং লোকাল credentials.json থাকে
    if not creds or not creds.valid:
        if os.path.exists("credentials.json"):
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        else:
            if not creds:
                raise Exception("❌ Blogger API Credentials and Token not found in Environment or Local Files.")

    return build("blogger", "v3", credentials=creds)


def create_json_ld(title, description, image_url):
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": description or title,
        "image": [image_url] if image_url else [],
        "author": {
            "@type": "Organization",
            "name": "TechBangla"
        },
        "publisher": {
            "@type": "Organization",
            "name": "TechBangla",
            "logo": {
                "@type": "ImageObject",
                "url": "https://blogger.googleusercontent.com/img/b/R29vZ2xl/"
            }
        },
        "datePublished": datetime.now().isoformat(),
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": "https://techbangla996.blogspot.com"
        }
    }

    return f'<script type="application/ld+json">\n{json.dumps(schema, ensure_ascii=False)}\n</script>\n'


def create_post(title, content, labels=None, search_description=None, image_url=None):
    service = get_service()

    # লেবেল নিখুঁতভাবে পার্স ও ক্লিন করার চূড়ান্ত লজিক
    formatted_labels = []
    if labels:
        if isinstance(labels, str):
            raw_list = labels.split(',')
        elif isinstance(labels, list):
            raw_list = []
            for item in labels:
                if isinstance(item, str):
                    raw_list.extend(item.split(','))
                else:
                    raw_list.append(str(item))
        else:
            raw_list = [str(labels)]

        for tag in raw_list:
            cleaned = tag.strip()
            cleaned = cleaned.replace('"', '').replace("'", "").strip(',')
            if cleaned and cleaned not in formatted_labels:
                formatted_labels.append(cleaned)

    schema = create_json_ld(title, search_description, image_url)

    image_html = ""
    if image_url:
        image_html = f'''
<div class="separator" style="clear: both; text-align: center; margin-bottom: 25px;">
    <a href="{image_url}" style="margin-left: 1em; margin-right: 1em;">
        <img border="0" data-original-height="675" data-original-width="1200" src="{image_url}" alt="{title}" title="{title}" loading="eager" width="1200" height="675" style="max-width:100%; height:auto; border-radius:8px;" />
    </a>
</div>
<br/>
'''

    final_content = schema + image_html + content

    post = {
        "kind": "blogger#post",
        "title": title,
        "content": final_content
    }

    # ব্লগার API-তে লেবেলগুলো নিশ্চিতভাবে পাইথন লিস্ট আকারে পাস করা হচ্ছে
    if formatted_labels:
        post["labels"] = formatted_labels

    if search_description:
        post["searchDescription"] = search_description

    result = service.posts().insert(
        blogId=BLOG_ID,
        body=post,
        isDraft=False
    ).execute()

    print("Published successfully:")
    print(result.get("url"))

    save_post(
        title,
        result.get("url", ""),
        formatted_labels[0] if formatted_labels else "Technology"
    )

    return result
