import requests
import os


class InstagramService:
    def __init__(self):
        self.access_token = os.environ["ACCESS_TOKEN"]

    def upload_image_to_instagram(self, image_path, caption):
        # Instagram Graph API URL'si
        url = "https://graph.facebook.com/v12.0/me/media"

        # Resim dosyasını aç ve yükle
        with open(image_path, 'rb') as image_file:
            files = {
                'file': image_file,
                'caption': caption,
                'access_token': self.access_token
            }
            response = requests.post(url, files=files)

        if response.status_code == 200:
            media_id = response.json().get("id")
            print(f"Resim başarıyla yüklendi. Media ID: {media_id}")

            return media_id
        else:
            print("Resim yükleme başarısız oldu:", response.text)
            return None

    def publish_image(self, media_id):
        # Resmi yayınlamak için API isteği
        url = f"https://graph.facebook.com/v12.0/{media_id}/publish"
        response = requests.post(url, params={'access_token': self.access_token})

        if response.status_code == 200:
            print("Resim başarıyla paylaşıldı.")
        else:
            print("Resim paylaşımı başarısız oldu:", response.text)
