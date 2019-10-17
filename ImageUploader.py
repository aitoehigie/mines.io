from PIL import Image
import base64
import requests
import mimetypes
from io import BytesIO
import redis
import socket
from uuid import uuid4

REDIS_CONNECTION = redis.Redis()
IMAGE_FILE_TYPES = ["image/jpg", "image/jpeg", "image/png", "image/gif", "image/tiff", "image/psd", "image/ai", "image/eps", "image/indd", "image/raw"]

class ImageUploader():

    def __init__(self):
        self.dimension = [0,0]

    def cache_image_in_memory(self, image_url, image):
        REDIS_CONNECTION.set(image_url, image)

    def upload_to_servers(self, image_file):
        response = requests.get(image_file)
        content_type = response.headers["content-type"]
        if content_type in IMAGE_FILE_TYPES:
            with Image.open(BytesIO(response.content)) as image:
                img = BytesIO()
                image.save(img, format="JPEG")
                img_str = base64.b64encode(img.getvalue())
                image_file_url = socket.gethostbyname(socket.gethostname()) + "_" + str(uuid4())
                self.cache_image_in_memory(image_file_url, img_str)
                return image_file_url
        else:
            raise Exception("That is not a valid image filetype")

    def upload(self, image_file, max_width=50000, max_height=50000):
        test = {}
        test["max_width"] = max_width
        test["max_height"] = max_height
        if not self.validate(image_file, test):
            return "Not Valid"
        image_url = REDIS_CONNECTION.get(image_file)
        if not image_url:
            image_url = self.upload_to_servers(image_file)
        return image_url
        

    def validate(self, image_file, test):
        response = requests.get(image_file)
        img = Image.open(BytesIO(response.content))
        file_width, file_height = img.size
        if image_file:
            self.dimension[0] = file_width
            self.dimension[1] = file_height
            max_width = test.get("max_width")
            max_height = test.get("max_height")
            if self.dimension[0] > 0:
                if self.dimension[0] <= max_width and self.dimension[0] > 1:
                    if self.dimension[1] > 0:
                        if self.dimension[1] <= max_height and self.dimension[1] > 1:
                            return True
                        return False
                    else:
                        raise Exception("Invalid height")
                return False
            else:
                raise Exception("Invalid width")
        else:
            raise Exception("image_file is null")


