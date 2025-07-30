import os
import base64
import requests
from urllib.parse import urlparse

class NoApiKey(Exception):
    pass

class Error(Exception):
    pass

class APIError(Exception):
    pass

class RemoveBg:
    def __init__(self, api_key=None):
        if not api_key:
            raise NoApiKey()
        self.api_key = api_key

    def remove(self, input_path=None, output_path=None, url=None, base64_image=None, allow_redirects=None):
        data = {"size": "auto"}
        files = None

        if input_path:
            if not os.path.isfile(input_path):
                raise FileNotFoundError()
            if not output_path:
                output_path = input_path
            with open(input_path, 'rb') as image_file:
                files = {"image_file": image_file.read()}
        elif url:
            try:
                if allow_redirects is False:
                    response = requests.head(url, allow_redirects=False)
                else:
                    response = requests.head(url)
                if response.status_code != 200 or not response.headers.get('Content-Type', '').startswith('image/'):
                    raise Error("You must provide a direct link, this is not a direct link to an image.")
                data["image_url"] = url
            except:
                raise Error("Invalid url")
        elif base64_image:
            try:
                image_data = base64.b64decode(base64_image)
                kind = filetype.guess(image_data)
                if not kind or not kind.mime.startswith("image/"):
                    raise Error("Invalid base64")
                data["image_file_b64"] = base64_image
            except Exception as e:
                raise Error(e)
            if not output_path:
                raise Error("You must provide an output path for base64.")
        else:
            raise Error("Invalid base64")

        response = requests.post(
            "https://api.remove.bg/v1.0/removebg",
            data=data,
            files={"image_file": image_data} if files is None and base64_image else files,
            headers={"X-Api-Key": self.api_key},
        )

        if response.status_code == 200:
            with open(output_path, 'wb') as out_file:
                out_file.write(response.content)
            return output_path
        else:
            raise APIError(f"{response.status_code} - {response.text}")