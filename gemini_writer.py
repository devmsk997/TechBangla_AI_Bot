import os
from google import genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def generate_article(topic, category, keywords):
    """
    Gemini 2.5 Flash ব্যবহার করে SEO ফ্রেন্ডলি বাংলা আর্টিকেল তৈরি করার ফাংশন।
    main.py ফাইলের সাথে সামঞ্জস্য রেখে ফাংশনের নাম ও আর্গুমেন্ট ঠিক করা হয়েছে।
    """
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    keywords_str = ", ".join(keywords) if isinstance(keywords, list) else str(keywords)
    current_year = "2026"  # ২০২৬ সাল নিশ্চিত করতে

    prompt = f"""
You are an expert SEO Tech Blogger for TechBangla.
Write a comprehensive, engaging, and fully SEO-optimized blog post in Bengali about: '{topic}'.
Category: {category}
Target Keywords: {keywords_str}

STRICT REQUIREMENTS:
1. Current Year is strictly {current_year}. NEVER use 2024 or 2025 anywhere in the title, headers, or body text.
2. Output ONLY clean HTML tags (<h2>, <h3>, <p>, <ul>, <li>, <b>, <table>, <tr>, <td>, <br/>). Do NOT use Markdown (no **, ###).
3. Do NOT add any internal links inside the content. (Internal links will be appended safely by Python).
4. MUST include at least 3 high-authority external DOFOLLOW links (e.g., <a href="https://blog.google" target="_blank">Google Blog</a>, <a href="https://support.apple.com" target="_blank">Apple Support</a>). Do NOT use rel="nofollow".

Output Format MUST be exactly:

TITLE: [SEO Title in Bengali referencing {current_year}]

SEARCH_DESCRIPTION: [150 characters summary in Bengali]

LABELS: {category}, সাইবার নিরাপত্তা, টেক নিউজ

CONTENT:
[Introductory text in Bengali]

<h2>[Header 1 in Bengali]</h2>
[Details]

<h2>[Header 2 in Bengali]</h2>
[Details]

<h2>তুলনামূলক বিশ্লেষণ</h2>
<table border="1" style="width:100%; border-collapse: collapse; text-align: left; margin: 15px 0;">
  <tr style="background-color: #f2f2f2;">
    <th style="padding: 8px;">বিষয়</th>
    <th style="padding: 8px;">অপশন A</th>
    <th style="padding: 8px;">অপশন B</th>
  </tr>
  <tr>
    <td style="padding: 8px;">...</td>
    <td style="padding: 8px;">...</td>
    <td style="padding: 8px;">...</td>
  </tr>
</table>

<h2>উপসংহার</h2>
[Conclusion text in Bengali]
"""

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        print(f"Error generating content via Gemini: {e}")
        raise e
