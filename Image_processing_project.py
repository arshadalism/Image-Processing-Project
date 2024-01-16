import requests
from PIL import Image, ImageOps, ImageDraw, ImageFont
from io import BytesIO
import os
from dotenv import load_dotenv

load_dotenv()

API_key = os.getenv("API_Key")

if os.path.exists("images") is False:
    os.mkdir("images")

names = []
images_list = []
collection_list =[]


def save_image(name, image_file):
    if not os.path.exists("images"):
        print('inside of save_file')
        os.mkdir("images")
    img1 = image_file.save(f"{name}.jpg", "JPEG")
    names.append(f"{name}.jpg")


def pexels_photos(query_name):
    base_url = "https://api.pexels.com/v1/search"
    headers = {
        "Authorization": API_key
    }
    params = {
        "query": query_name,  # Ocean | Tiger | Pears
        "size": "large",  # large | small | medium
        "orientation": "portrait",  # landscape | portrait | square
        "color": "black",  # red | orange | pink | black
        "page": 1,
        "per_page": 4
    }

    response = requests.get(url=base_url, headers=headers, params=params)
    data = response.json()
    if response.status_code != 200:
        print("Error:", response.status_code)
        return
    photos = data["photos"]
    for photo in photos:
        image_url = photo["src"]["medium"]
        response_image = requests.get(image_url)
        img = Image.open(BytesIO(response_image.content))
        image_dim = img.size
        # print(image_dim)
        image_ratio = float(image_dim[1] / image_dim[0])
        # print(image_ratio)
        name = f"{params['query']}_{photo['id']}"
        save_image(name, img)
    return names


def curated_photos():
    base_url = "https://api.pexels.com/v1/curated"
    headers = {
        "Authorization": API_key
    }
    params = {
        "page": 1,
        "per_page": 2
    }
    curated_response = requests.get(url=base_url, headers=headers, params=params)
    curated_data = curated_response.json()
    photos_curated = curated_data["photos"]
    image_url = photos_curated[0]["src"].get("tiny")
    response_image = requests.get(image_url)
    img = Image.open(BytesIO(response_image.content))
    # img.show()


def college_photo(my_list):
    max_width = 0
    max_height = 0

    for image_path in my_list:
        img = Image.open(image_path)
        width, height = img.size
        max_width = max(max_width, width)
        max_height = max(max_height, height)

    for i, image_path in enumerate(my_list):
        img = Image.open(image_path)
        img = img.resize((max_width, max_height))
        my_list[i] = img

    college_width = max_width * 2
    college_height = max_height * 2
    positions = [(0, 0), (max_width, 0), (0, max_height), (max_width, max_height)]
    collage = Image.new('RGB', (college_width, college_height))

    for i, img in enumerate(my_list):
        collage.paste(img, positions[i])

    collage.save(f"{search}.jpg")
    collage.show()


def collage_photo2(path_list):
    all_imgs = [Image.open(path) for path in path_list]
    width,height = all_imgs[0].size
    positions = [(0, 0), (width, 0), (0, height), (width, height)]

    collage = Image.new('RGB', (width*2, height*2))
    for i, img in enumerate(all_imgs):
        img.show()
        collage.paste(img, positions[i])

    collage.show()


search = 'Medina'  # This is the search place
my_list = pexels_photos(search)
collage_photo2(my_list)
