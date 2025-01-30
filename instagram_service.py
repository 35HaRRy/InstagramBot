import requests
import logging
import os

from instabot import Bot
from PIL import Image


class InstagramService:
    def __init__(self):
        self.bot = Bot()
        
        userName = os.environ["INSTAGRAM_USERNAME"]
        password = os.environ["INSTAGRAM_PASSWORD"]

        """Instagram hesabına giriş yapar"""
        try:
            self.bot.login(username=userName, password=password)
        except Exception as e:
            logging.error(f"Giriş hatası: {str(e)}")
    
    def upload_photo(self, image_path, caption=""):
        """Fotoğrafı Instagram'a yükler"""
        try:
            # Resmi hazırla
            prepared_image = self.prepare_image(image_path)
            if not prepared_image:
                return False
            
            # Yüklemeyi gerçekleştir
            upload_status = self.bot.upload_photo(
                prepared_image,
                caption=caption
            )
            
            # Geçici dosyayı temizle
            if os.path.exists(prepared_image):
                os.remove(prepared_image)
            
            # config dosyasını temizle
            if os.path.exists(f"{prepared_image}.REMOVE_ME"):
                os.remove(f"{prepared_image}.REMOVE_ME")
            
            return upload_status
        except Exception as e:
            logging.error(f"Yükleme hatası: {str(e)}")
            return False
    
    def logout(self):
        """Hesaptan çıkış yapar"""
        try:
            self.bot.logout()
            return True
        except:
            return False

    # def upload_image_to_instagram(self, image_path, caption):
    #     # Instagram Graph API URL'si
    #     url = "https://graph.facebook.com/v12.0/me/media"

    #     # Resim dosyasını aç ve yükle
    #     with open(image_path, 'rb') as image_file:
    #         files = {
    #             'file': image_file,
    #             'caption': caption,
    #             'access_token': self.access_token
    #         }
    #         response = requests.post(url, files=files)

    #     if response.status_code == 200:
    #         media_id = response.json().get("id")
    #         logging.info(f"Resim başarıyla yüklendi. Media ID: {media_id}")

    #         return media_id
    #     else:
    #         logging.error(f"Resim yükleme başarısız oldu: {response.text}")
    #         return None

    # def publish_image(self, media_id):
    #     # Resmi yayınlamak için API isteği
    #     url = f"https://graph.facebook.com/v12.0/{media_id}/publish"
    #     response = requests.post(url, params={'access_token': self.access_token})

    #     if response.status_code == 200:
    #         logging.info("Resim başarıyla paylaşıldı.")
    #     else:
    #         logging.error("Resim paylaşımı başarısız oldu:", response.text)
