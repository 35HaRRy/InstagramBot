import logging
# import os

from dotenv import load_dotenv

from image_service import ImageService
# from .instagram_service import InstagramService


if __name__ == "__main__":
    load_dotenv()

    logging.info('Instagram post function triggered')

    # try:
    image_service = ImageService()
    image_path = image_service.create_image()

    if image_path:
        caption = image_service.last_used_quote

        # instagram_service = InstagramService()
        # media_id = instagram_service.upload_image_to_instagram(image_path, caption)

        # if media_id:
        #     instagram_service.publish_image(media_id)

        # os.remove(image_path)
    else:
        logging.error('Failed to create image')
    # except Exception as e:
    #     logging.error(f'Error in Instagram post function: {str(e)}')
