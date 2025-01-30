import logging
# import os

from dotenv import load_dotenv

from instagram_service import InstagramService
from image_service import ImageService
from quote_service import QuoteService


if __name__ == "__main__":
    load_dotenv()

    logging.info('Instagram post function triggered')

    # try:
    quote_service = QuoteService()
    quote = quote_service.get_unshared_quote()

    image_service = ImageService()
    image_path = image_service.create_image(quote["text"])

    if image_path:
        logging.info(f'Image created successfully: {image_path}')

        instagram_service = InstagramService()
        # media_id = instagram_service.upload_image_to_instagram(image_path, quote["text"])
        upload_status = instagram_service.upload_image_to_instagram(image_path, quote["text"])

        # if media_id:
        #     instagram_service.publish_image(media_id)
        #     quote_service.mark_quote_as_shared(quote["_id"])

        #     logging.info('Image published successfully')
        # else:
        #     logging.error('Failed to upload image to Instagram')

        # os.remove(image_path)

        if upload_status:
            logging.info('Image published successfully')
        else:
            logging.error('Failed to upload image to Instagram')
    else:
        logging.error('Failed to create image')
    # except Exception as e:
    #     logging.error(f'Error in Instagram post function: {str(e)}')
