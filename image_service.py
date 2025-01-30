import os
import requests
import tempfile
import logging
import urllib.parse


class ImageService:
    def __init__(self):
        self.leonardo_api_key = os.environ["LEONARDO_AI_API_KEY"]

    def generate_image_with_leonardo(self, prompt):
        """Leonardo.ai API'sini kullanarak resim oluştur"""
        headers = {
            "Authorization": f"Bearer {self.leonardo_api_key}",
            "Content-Type": "application/json"
        }

        # Leonardo.ai API endpoint ve parametreleri
        url = "https://cloud.leonardo.ai/api/rest/v1/generations"
        data = {
            "prompt": prompt,
            "modelId": "your_selected_model_id",  # Leonardo.ai model ID'si
            "width": 1080,  # Instagram için uygun genişlik
            "height": 1080  # Instagram için uygun yükseklik
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            generation_id = response.json()["generationId"]

            # Resim oluşturulana kadar bekle
            while True:
                status_response = requests.get(
                    f"{url}/{generation_id}",
                    headers=headers
                )
                if status_response.status_code == 200:
                    result = status_response.json()
                    if result["status"] == "COMPLETE":
                        image_url = result["generations"][0]["imageUrl"]
                        return image_url

        return None

    def generate_image_with_pollinations(self, prompt):
        parsed_prompt = prompt.replace(" ", "-")
        image_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(parsed_prompt)}"

        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpeg")

            for chunk in response.iter_content(1024):
                temp_file.write(chunk)

            temp_file.close()
            print(temp_file.name)
            return temp_file.name

        return None

    def download_image(self, image_url):
        """Oluşturulan resmi geçici bir dosyaya indir"""
        response = requests.get(image_url)
        if response.status_code == 200:
            # Geçici dosya oluştur
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
            temp_file.write(response.content)
            temp_file.close()
            return temp_file.name
        return None

    def create_image(self, quote):
        """Ana resim oluşturma fonksiyonu"""
        try:
            if not quote:
                logging.error("No unshared quotes found")
                return None

            # Alıntıyı Leonardo.ai için prompt'a çevir
            prompt = f"Create an artistic interpretation of the quote: {quote}"

            image_url = self.generate_image_with_pollinations(prompt)
            if not image_url:
                logging.error("Failed to generate image with Leonardo.ai")
                return None

            image_path = self.download_image(image_url)
            if not image_path:
                logging.error("Failed to download generated image")
                return None

            return image_path
        except Exception as e:
            logging.error(f"Error in create_image: {str(e)}")
            return None
