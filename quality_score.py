import re




def calculate_quality_score(
        title,
        content
):


    score = 100


    checks = {}



    # Word count

    words = len(
        content.split()
    )


    if words < 1000:

        score -= 20

        checks["word_count"] = "Low"

    else:

        checks["word_count"] = "Good"





    # Heading check

    h2 = len(
        re.findall(
            "<h2",
            content
        )
    )


    if h2 < 3:

        score -= 10

        checks["headings"] = "Need more headings"

    else:

        checks["headings"] = "Good"






    # FAQ check


    if "FAQ" in content or "faq" in content:


        checks["faq"] = "Present"


    else:


        score -= 10

        checks["faq"] = "Missing"






    # Conclusion check


    if "Conclusion" in content or "উপসংহার" in content:


        checks["conclusion"] = "Present"


    else:


        score -= 10

        checks["conclusion"] = "Missing"






    if score < 0:

        score = 0




    return {

        "score": score,

        "details": checks

    }