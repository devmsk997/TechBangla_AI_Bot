import google.generativeai as genai

def generate_blog_content(topic, category, gemini_api_key):
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    current_year = "2026"  # ফিক্সড ২০২৬ সাল

    prompt = f"""
You are an expert SEO Tech Blogger for TechBangla.
Write a comprehensive, engaging, and fully SEO-optimized blog post in Bengali about: '{topic}'.
Category: {category}

STRICT REQUIREMENTS:
1. Current Year is strictly {current_year}. NEVER use 2024 or 2025 anywhere in the title, headers, or body text.
2. Output ONLY clean HTML tags (<h2>, <ul>, <li>, <b>, <table>, <tr>, <td>, <br/>). Do NOT use Markdown (no **, ###).
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
    response = model.generate_content(prompt)
    return response.text
