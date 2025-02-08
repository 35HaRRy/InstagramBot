import urllib.parse
import webbrowser
import requests
import time
import os

from http.server import HTTPServer, BaseHTTPRequestHandler
from dotenv import load_dotenv

from facebook_business.adobjects.iguser import IGUser
from facebook_business.api import FacebookAdsApi


class InstagramStoryUploader:
    def __init__(self, access_token):
        """
        Initialize the uploader with required credentials
        """

        self.app_id = os.environ["INSTAGRAM_APP_ID"]
        self.app_secret = os.environ["INSTAGRAM_APP_SECRET"]
        self.access_token = access_token
        self.instagram_account_id = os.environ["INSTAGRAM_ACCOUNT_ID"]

        # Initialize the Facebook API
        FacebookAdsApi.init(self.app_id, self.app_secret, self.access_token)

    def upload_story(self, image_url, caption=""):
        """
        Upload a story to Instagram using the Graph API
        """
        try:
            # Get the Instagram user instance
            ig_user = IGUser(self.instagram_account_id)

            # First, create a container for the story
            story_container = ig_user.create_media(
                params={
                    'image_url': image_url,
                    'caption': caption,
                    'media_type': 'STORIES'
                }
            )

            # Get the container ID
            container_id = story_container['id']

            # Wait for a moment to ensure the container is ready
            time.sleep(5)

            # Publish the story
            ig_user.publish_media(
                params={
                    'creation_id': container_id
                }
            )

            return True, "Story başarıyla yüklendi!"

        except Exception as e:
            return False, f"Hata oluştu: {str(e)}"

    def upload_story_with_local_image(self, image_path, caption=""):
        """
        Upload a story using a local image file
        """
        try:
            # Upload image to temporary hosting (örnek olarak imgbb kullanabilirsiniz)
            # Bu kısım için ayrı bir servis kullanmanız gerekir
            image_url = self._upload_to_temporary_hosting(image_path)

            return self.upload_story(image_url, caption)

        except Exception as e:
            return False, f"Resim yükleme hatası: {str(e)}"


class TokenHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle the redirect from Facebook OAuth"""
        # Parse the URL query parameters
        query_components = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        
        # Get the authorization code
        if 'code' in query_components:
            self.server.auth_code = query_components['code'][0]
            
            # Send success response
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Authorization successful! You can close this window.")
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Authorization failed!")


class InstagramTokenGenerator:
    def __init__(self):
        self.app_id = os.environ["INSTAGRAM_APP_ID"]
        self.app_secret = os.environ["INSTAGRAM_APP_SECRET"]
        self.redirect_uri = os.environ["INSTAGRAM_REDIRECT_URI"]
        self.auth_code = None
        self.access_token = None
        self.long_lived_token = None

    def get_auth_url(self):
        """Generate the OAuth URL for user authorization"""
        base_url = "https://www.facebook.com/v12.0/dialog/oauth"
        scope = "instagram_basic,instagram_content_publish,pages_read_engagement"

        auth_url = (
            f"{base_url}?"
            f"client_id={self.app_id}&"
            f"redirect_uri={self.redirect_uri}&"
            f"scope={scope}&"
            f"response_type=code"
        )
        return auth_url

    def start_auth_server(self):
        """Start local server to handle OAuth redirect"""
        server_address = ('', 8000)  # Port 8000
        httpd = HTTPServer(server_address, TokenHandler)
        httpd.auth_code = None

        print("Waiting for authorization...")
        while httpd.auth_code is None:
            httpd.handle_request()

        self.auth_code = httpd.auth_code
        return self.auth_code

    def get_short_lived_token(self):
        """Exchange authorization code for short-lived access token"""
        token_url = "https://graph.facebook.com/v12.0/oauth/access_token"

        params = {
            "client_id": self.app_id,
            "client_secret": self.app_secret,
            "redirect_uri": self.redirect_uri,
            "code": self.auth_code
        }

        response = requests.get(token_url, params=params)
        if response.status_code == 200:
            self.access_token = response.json()["access_token"]
            return self.access_token
        else:
            raise Exception(f"Token alınamadı: {response.text}")

    def get_long_lived_token(self):
        """Exchange short-lived token for long-lived access token"""
        if not self.access_token:
            raise Exception("Önce kısa süreli token alınmalı!")

        token_url = "https://graph.facebook.com/v12.0/oauth/access_token"

        params = {
            "grant_type": "fb_exchange_token",
            "client_id": self.app_id,
            "client_secret": self.app_secret,
            "fb_exchange_token": self.access_token
        }

        response = requests.get(token_url, params=params)
        if response.status_code == 200:
            self.long_lived_token = response.json()["access_token"]
            return self.long_lived_token
        else:
            raise Exception(f"Uzun süreli token alınamadı: {response.text}")


def main():
    load_dotenv()

    generator = InstagramTokenGenerator()

    # Yetkilendirme URL'ini al ve tarayıcıda aç
    auth_url = generator.get_auth_url()
    webbrowser.open(auth_url)

    try:
        # Yetkilendirme kodunu al
        auth_code = generator.start_auth_server()
        print(f"Auth code alındı: {auth_code}")

        # Kısa Süreli Token Al
        short_lived_token = generator.get_short_lived_token()
        print(f"Kısa süreli token alındı: {short_lived_token}")

        # Uzun süreli token al
        long_lived_token = generator.get_long_lived_token()
        print(f"Uzun süreli token alındı: {long_lived_token}")

    except Exception as e:
        print(f"Hata oluştu: {str(e)}")

    uploader = InstagramStoryUploader(generator.access_token)

    # Hikaye paylaş
    image_url = "https://ssl.gstatic.com/onebox/media/sports/logos/TWjoccvTU4JXZJZ3aW3cVg_64x64.png"
    caption = "Test story!"

    success, message = uploader.upload_story(image_url, caption)
    print(message)


if __name__ == "__main__":
    main()
