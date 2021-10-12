import pathlib
import shutil
import requests
import os
import sys
import webbrowser
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


location = ""
if(sys.argv[1]):
    location = sys.argv[1]
else:
    input("url or path of image: ")

file = ""
if(location.startswith("http")):
    download(location)
    file = f'{pathlib.Path(__file__).parent.resolve()}\image.{location.split("/")[-1].split(".")[-1].lower()}'
else:
    file = location

text = getText(file).strip().replace("\n\n", "")

urls = {"http": [], "https": []}

for i in text.split(" "):
    if i.startswith("https"):
        urls["https"].append(i)
    elif i.startswith("http"):
        urls["http"].append(i)

print(f'{len(urls["https"]) + len(urls["http"])} URLs found')

for i in urls["https"]:
    if input(f"Open secure link: {i}?").startswith("y"):
        webbrowser.open_new_tab(i)
        print("Opening...")

for i in urls["http"]:
    if input(f"Open insecure link: {i}?").startswith("y"):
        webbrowser.open_new_tab(i)
        print("Opening...")

print(f"Data found:\n{text}")

os.remove(file)
print("Image succesfully undownloaded")
