from PIL import Image
import os



def check_image_quality(image_file):

    if not image_file:

        return False



    if not os.path.exists(image_file):

        print("Image file missing")

        return False



    try:


        image = Image.open(
            image_file
        )


        width, height = image.size



        file_size = os.path.getsize(
            image_file
        )



        print(
            "Image size:",
            width,
            "x",
            height
        )


        print(
            "Image file size:",
            file_size,
            "bytes"
        )



        # Minimum resolution

        if width < 600 or height < 400:


            print(
                "Image resolution too low"
            )

            return False




        # Minimum file size

        if file_size < 10000:


            print(
                "Image file too small"
            )

            return False




        # Verify image

        image.verify()



        print(
            "Image quality OK"
        )


        return True




    except Exception as e:


        print(
            "Bad image:",
            e
        )


        return False