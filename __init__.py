import datetime
import logging
import os

import azure.functions as func

from dotenv import load_dotenv

from instagram_service import InstagramService
from image_service import ImageService
from quote_service import QuoteService


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()

    load_dotenv()

    logging.info('Instagram post function triggered')

    try:
        quote_service = QuoteService()
        quote = quote_service.get_unshared_quote()

        image_service = ImageService()
        image_path = image_service.create_image(quote["text"])

        if image_path:
            logging.info(f'Image created successfully: {image_path}')

            instagram_service = InstagramService()
            upload_status = instagram_service.upload_photo(image_path, quote["text"])

            if upload_status:
                if os.path.exists(image_path):
                    os.remove(image_path)

                logging.info('Image published successfully')
            else:
                logging.error('Failed to upload image to Instagram')
        else:
            logging.error('Failed to create image')
    except Exception as e:
        logging.error(f'Error in Instagram post function: {str(e)}')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
