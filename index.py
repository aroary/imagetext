import pathlib
import shutil
import requests
from PIL import Image
from pytesseract import pytesseract

pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def getText(path):
    return pytesseract.image_to_string(Image.open(path))[:-1]


def download(url):
    filename = f"image.{url.split('/')[-1].split('.')[-1].lower()}"
    image = requests.get(url, stream=True)
    if image.status_code == 200:
        image.raw.decode_content = True
        with open(filename, 'wb') as file:
            shutil.copyfileobj(image.raw, file)
        print('Image successfully downloaded')
    else:
        print('Problem getting image')


location = input("url or path of image: ")
file = ""
if(location.startswith("http")):
    download(location)
    file = f'{pathlib.Path(__file__).parent.resolve()}\image.{location.split("/")[-1].split(".")[-1].lower()}'
else:
    file = location

print(getText(file))