from google import genai
import time

from config import GEMINI_API_KEY



client = genai.Client(
    api_key=GEMINI_API_KEY
)



MODELS = [

    "gemini-3.6-flash"

]



MAX_RETRY = 2





def generate_article(topic, category, keywords):


    primary_keyword = keywords.get(
        "primary_keyword",
        topic
    )


    related_keywords = keywords.get(
        "related_keywords",
        []
    )




    prompt = f"""

আপনি TechBangla-এর জন্য একজন professional SEO বাংলা Technology writer।


Topic:
{topic}


Category:
{category}



Primary Keyword:

{primary_keyword}



Related Keywords:

{related_keywords}





আপনাকে অবশ্যই নিচের format অনুসরণ করতে হবে।



TITLE:

SEO friendly বাংলা title লিখুন।



SEARCH_DESCRIPTION:

150-160 character এর description লিখুন।



LABELS:

৩-৫টি label comma দিয়ে লিখুন।



CONTENT:

এর পরে HTML format-এ সম্পূর্ণ article লিখুন।





Rules:

- বাংলা ভাষায় লিখুন
- Unique content লিখুন
- 1500+ শব্দ
- SEO friendly করুন
- H2 H3 heading ব্যবহার করুন
- FAQ section যোগ করুন
- Conclusion যোগ করুন
- Keyword stuffing করবেন না
- Reader friendly করুন




IMPORTANT:

TITLE:
SEARCH_DESCRIPTION:
LABELS:

এই format পরিবর্তন করবেন না।

CONTENT: এর পরে শুধু article লিখবেন।

"""




    last_error = None




    for model in MODELS:


        for attempt in range(MAX_RETRY):


            try:


                print(
                    f"Trying model: {model} | Attempt {attempt+1}"
                )



                response = client.models.generate_content(

                    model=model,

                    contents=prompt

                )



                if response.text:


                    print(
                        "Article generated successfully"
                    )


                    return response.text






            except Exception as e:



                last_error = e


                error_text = str(e)



                print(

                    "Gemini Error:",

                    error_text

                )





                # Quota error

                if (

                    "429" in error_text

                    or

                    "RESOURCE_EXHAUSTED" in error_text

                ):


                    print(

                        "Gemini quota finished. Stop."

                    )


                    raise Exception(

                        "Gemini API quota exhausted. Change API key or wait for reset."

                    )






                # Model error

                if (

                    "404" in error_text

                    or

                    "NOT_FOUND" in error_text

                ):


                    print(

                        "Model unavailable."

                    )


                    break





                time.sleep(5)







    raise Exception(

        "Gemini generation failed: "

        + str(last_error)

    )