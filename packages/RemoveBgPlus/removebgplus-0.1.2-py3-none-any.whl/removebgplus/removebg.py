import os
import base64
import requests
import filetype

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

    def remove_from_file(self, input_path, output_path):
        if not os.path.isfile(input_path):
            raise FileNotFoundError()
        with open(input_path, 'rb') as image_file:
            files = {"image_file": image_file.read()}
        return self._send_request(files=files, output_path=output_path)

    def remove_from_url(self, url, output_path, allow_redirects=True):
        try:
            response = requests.head(url, allow_redirects=allow_redirects)
            if response.status_code != 200 or not response.headers.get('Content-Type', '').startswith('image/'):
                raise Error("You must provide a direct link, this is not a direct link to an image.")
        except:
            raise Error("Invalid url")
        data = {"size": "auto", "image_url": url}
        return self._send_request(data=data, output_path=output_path)

    def remove_from_base64(self, base64_string, output_path):
        if not isinstance(base64_string, str):
            raise Error("You must provide a base64-encoded string")
        try:
            decoded = base64.b64decode(base64_string)
        except Exception:
            raise Error("Invalid base64 string")
        kind = filetype.guess(decoded)
        if not kind or not kind.mime.startswith("image/"):
            raise Error("Invalid image bytes")
        data = {"size": "auto", "image_base64": base64_string}
        return self._send_request(data=data, output_path=output_path)

    def _send_request(self, data=None, files=None, output_path=None):
        response = requests.post(
            "https://api.remove.bg/v1.0/removebg",
            data=data or {"size": "auto"},
            files={"image_file": files["image_file"]} if files else None,
            headers={"X-Api-Key": self.api_key},
        )
        if response.status_code == 200:
            with open(output_path, 'wb') as out_file:
                out_file.write(response.content)
            return output_path
        else:
            raise APIError(f"{response.status_code} - {response.text}")