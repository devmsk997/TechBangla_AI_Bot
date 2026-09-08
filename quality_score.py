import re

def calculate_quality_score(title, content):
    score = 100
    checks = {}

    # ১. HTML ট্যাগ সরিয়ে কেবল আসল বাংলা শব্দের সংখ্যা গণনা
    clean_text = re.sub(r'<[^>]+>', '', content)
    words = len(clean_text.split())

    if words < 600:
        score -= 20
        checks["word_count"] = f"Low ({words} words)"
    elif words < 1000:
        score -= 10
        checks["word_count"] = f"Moderate ({words} words)"
    else:
        checks["word_count"] = f"Good ({words} words)"

    # ২. Heading Check (H2 ট্যাগ অন্তত ৩টি আছে কিনা)
    h2_count = len(re.findall(r'<h2', content, re.IGNORECASE))
    if h2_count < 3:
        score -= 10
        checks["headings"] = f"Need more H2 (Found: {h2_count})"
    else:
        checks["headings"] = f"Good ({h2_count} H2 tags)"

    # ৩. FAQ Check (বাংলা ও ইংরেজি উভয় শব্দ সাপোর্ট করবে)
    faq_keywords = ["faq", "প্রশ্নোত্তর", "সাধারণ প্রশ্ন", "FAQ"]
    if any(keyword in content for keyword in faq_keywords):
        checks["faq"] = "Present"
    else:
        score -= 10
        checks["faq"] = "Missing"

    # ৪. Conclusion Check (বাংলা ও ইংরেজি)
    conclusion_keywords = ["উপসংহার", "conclusion", "শেষ কথা", "পরিশেষে"]
    if any(keyword in content for keyword in conclusion_keywords):
        checks["conclusion"] = "Present"
    else:
        score -= 10
        checks["conclusion"] = "Missing"

    # ৫. Table Presence Check (SEO এর জন্য গুরুত্বপূর্ণ)
    if "<table" in content.lower():
        checks["table"] = "Present"
    else:
        score -= 10
        checks["table"] = "Missing Table"

    # ৬. External Link Check
    if "<a href=" in content.lower():
        checks["external_links"] = "Present"
    else:
        score -= 10
        checks["external_links"] = "Missing External Links"

    # স্কোর যেন ০ এর নিচে না যায়
    score = max(0, score)

    return {
        "score": score,
        "details": checks
    }
