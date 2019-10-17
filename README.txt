Introduction
Mines.io image uploader API takes a url to an image file url as input and then uses the class to cache the image it’s supplied in memory, uploads to the server and sends back a new Url to reach the uploaded file. The API only support images.
Overview
Create a virtual environment (pipenv is prefered)
Install all dependencies in the requirements.txt file with 'pipenv run pip install -r requirements.txt'
run the API with 'python main.py'
Send the url as form data: key = 'url', value='[image link]'
You will receive the uploaded image link as a JSON image

POST /upload


