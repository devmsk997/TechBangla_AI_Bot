import re


from topic_cluster import choose_topic

from keyword_research import research_keywords

from gemini_writer import generate_article

from seo_optimizer import optimize_seo

from quality_score import calculate_quality_score

from duplicate_checker import check_duplicate

from image_generator import generate_image

from image_quality import check_image_quality

from github_image import upload_image

from blogger import create_post

from internal_linker import add_internal_links





def parse_article(ai_text):


    title = ""

    search_description = ""

    labels = []

    content = ""



    title_match = re.search(

        r"TITLE:\s*(.*)",

        ai_text

    )


    if title_match:

        title = title_match.group(1).strip()





    desc_match = re.search(

        r"SEARCH_DESCRIPTION:\s*(.*)",

        ai_text

    )


    if desc_match:

        search_description = desc_match.group(1).strip()





    label_match = re.search(

        r"LABELS:\s*(.*)",

        ai_text

    )


    if label_match:

        labels = [

            x.strip()

            for x in label_match.group(1).split(",")

        ]





    content_match = re.search(

        r"CONTENT:\s*(.*)",

        ai_text,

        re.DOTALL

    )


    if content_match:

        content = content_match.group(1).strip()



    return (

        title,

        search_description,

        labels,

        content

    )







def main():


    print("🚀 TechBangla AI Bot Started")



    # 1 Topic select

    topic, category = choose_topic()



    print("Topic:", topic)

    print("Category:", category)





    # 2 Keyword research

    keywords = research_keywords(

        category,

        topic

    )



    print(

        "Keywords:",

        keywords

    )






    # 3 Generate article

    ai_article = generate_article(

        topic,

        category,

        keywords

    )





    print(

        "Article generated successfully"

    )






    # 4 Parse article

    title, search_description, labels, content = parse_article(

        ai_article

    )





    if not title:

        title = topic





    print(

        "Title:",

        title

    )






    # 5 Internal linking


    content = add_internal_links(

        content,

        category

    )





    # 6 SEO

    seo = optimize_seo(

        title,

        content,

        category

    )





    if not search_description:


        search_description = seo[

            "search_description"

        ]







    # 7 Quality check


    quality = calculate_quality_score(

        title,

        content

    )



    print(

        "Quality Score:",

        quality["score"]

    )




    if quality["score"] < 60:


        print(

            "Quality too low. Cancelled."

        )

        return






    # 8 Duplicate check


    duplicate = check_duplicate(

        title,

        content

    )



    if duplicate["duplicate"]:


        print(

            "Duplicate article found."

        )

        return







    # 9 Image generation


    image_url = None



    for attempt in range(3):


        print(

            f"Generating image attempt: {attempt+1}"

        )


        image_file = generate_image(

            title

        )



        if not image_file:

            continue




        if check_image_quality(

            image_file

        ):


            print(

                "Image quality OK"

            )


            image_url = upload_image(

                image_file

            )


            break




        else:


            print(

                "Bad image. Regenerating..."

            )








    if not image_url:


        print(

            "Image failed. Posting without image."

        )







    # 10 Blogger publish


    create_post(

        title,

        content,

        labels,

        search_description,

        image_url

    )





    print(

        "✅ Bot Finished Successfully"

    )







if __name__ == "__main__":


    main()