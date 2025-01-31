import logging
import os

from instabot import Bot


class InstagramService:
    def __init__(self):
        userName = os.environ["INSTAGRAM_USERNAME"]
        password = os.environ["INSTAGRAM_PASSWORD"]

        self.bot = Bot()

        try:
            self.bot.login(username=userName, password=password)
        except Exception as e:
            logging.error(f"Giriş hatası: {str(e)}")

    def upload_photo(self, image_path, caption=""):
        """Fotoğrafı Instagram'a yükler"""
        try:
            upload_status = self.bot.upload_photo(
                image_path,
                caption=caption
            )

            self.bot.publish()

            return upload_status
        except Exception as e:
            logging.error(f"Yükleme hatası: {str(e)}")
            return False

    def logout(self):
        self.bot.logout()
        return True
