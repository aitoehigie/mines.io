from sanic import Sanic, request
from sanic.response import json

from imageuploader import ImageUploader

api = Sanic(__name__)

image = ImageUploader()

@api.route("/upload", methods=["GET", "POST"])
async def upload(request):
    url = request.form.get("url")
    response = image.upload(str(url))
    return json({"uploaded image link":response}, 200)

if __name__ == "__main__":
    api.run(host="0.0.0.0", port=5000)
