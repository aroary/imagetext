import sys
import os
import pathlib
import shutil
import requests
import colorama
import webbrowser
from PIL import Image
from pytesseract import pytesseract

colorama.init()

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
        print(colorama.Fore.GREEN + 'Image successfully downloaded')
    else:
        print(colorama.Fore.RED + 'Problem getting image')
    colorama.Style.RESET_ALL


def formatText(string):
    return string.strip().replace("\n\n", "")

location = ""
if(len(sys.argv) >= 2):
    location = sys.argv[1]
else:
    location = input("url or path of image: ")
    if len(location) < 1:
        print(colorama.Fore.YELLOW + "No image selected")
        colorama.Style.RESET_ALL

file = ""
if(location.startswith("http")):
    try:
        download(location)
        file = f'{pathlib.Path(__file__).parent.resolve()}\image.{location.split("/")[-1].split(".")[-1].lower()}'
    except:
        print(colorama.Fore.RED + 'Problem getting image')
        colorama.Style.RESET_ALL
elif len(location) < 1:
    sys.exit()
else:
    file = location

if len(file):
    text = formatText(getText(file))

    urls = {"http": [], "https": []}

    for i in text.split(" "):
        i = i.split("\n")[0]
        if i.startswith("https"):
            urls["https"].append(i)
        elif i.startswith("http"):
            urls["http"].append(i)

    print(colorama.Fore.YELLOW +
          f'{len(urls["https"]) + len(urls["http"])} URLs found')
    colorama.Style.RESET_ALL

    queue = []
    for i in urls["https"]:
        if input(f"Open secure link: {i}? ").startswith("y"):
            queue.append(i)

    for i in urls["http"]:
        if input(f"Open insecure link: {i}? ").startswith("y"):
            webbrowser.open_new_tab(i)
            print("Opening...")

    if(len(queue)):
        for i in queue:
            print(f"Opening {len(queue)} links...")
            webbrowser.open_new_tab(i)

    print(f"Data found:\n{text}")
else:
    print(colorama.Fore.YELLOW + "No text found")
    colorama.Style.RESET_ALL

if(os.path.exists(file)):
    os.remove(file)
    print("Image succesfully undownloaded")

colorama.Style.RESET_ALL
