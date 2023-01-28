import requests
from bs4 import BeautifulSoup
import json
import uuid
from official.models import Variant, BrandModel

items = []
filepaths = []


def get_data(url, brand_slug, brand_pk):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    for li in soup.find("div", class_="makers").find_all("li"):
        a_tag = li.find("a")
        img_tag = li.find("img")
        name = a_tag.find("strong").text
        photo_url = img_tag["src"]
        description = img_tag["title"]
        image = photo_url.replace("https://fdn2.gsmarena.com/vv/bigpic/", "models/" + brand_slug + "/")
        items.append(
            {
                "model": "official.brandmodel",
                "pk": str(uuid.uuid4()),
                "fields": {
                    "brand": brand_pk,
                    "image": image,
                    "name": name,
                    "slug": name.lower().replace(" ", "-"),
                    "description": description,
                    "is_mostselling": 0,
                },
            }
        )
    return items


def get_filepaths(url, brand_slug, brand_pk):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    for li in soup.find("div", class_="makers").find_all("li"):
        img_tag = li.find("img")
        photo_url = img_tag["src"]
        media_url = f"wget {photo_url}"
        # write to a text file one by one
        with open("scripts/media_urls.txt", "a") as f:
            f.write(media_url + "\n")


data = [
    {
        "brand_slug": "motorola",
        "brand_pk": 21,
        "urls": [
            "https://www.gsmarena.com/motorola-phones-4.php",
            "https://www.gsmarena.com/motorola-phones-f-4-0-p2.php",
            "https://www.gsmarena.com/motorola-phones-f-4-0-p3.php",
            "https://www.gsmarena.com/motorola-phones-f-4-0-p4.php",
            "https://www.gsmarena.com/motorola-phones-f-4-0-p5.php",
            "https://www.gsmarena.com/motorola-phones-f-4-0-p6.php",
            "https://www.gsmarena.com/motorola-phones-f-4-0-p7.php",
            "https://www.gsmarena.com/motorola-phones-f-4-0-p8.php",
            "https://www.gsmarena.com/motorola-phones-f-4-0-p9.php",
            "https://www.gsmarena.com/motorola-phones-f-4-0-p10.php",
            "https://www.gsmarena.com/motorola-phones-f-4-0-p11.php",
            "https://www.gsmarena.com/motorola-phones-f-4-0-p12.php",
        ],
    }
]


# def run():
#     final = []
#     for url in data:
#         for u in url["urls"]:
#             final += get_data(u, url["brand_slug"], url["brand_pk"])
#             get_filepaths(u, url["brand_slug"], url["brand_pk"])

#     with open("scripts/data.json", "w") as f:
#         json.dump(final, f, indent=4)


def run():
    for model in BrandModel.objects.all():
        if Variant.objects.filter(model=model).count() == 0:
            Variant.objects.create(
                brand_model=model,
                RAM="Standard",
                color="Standard",
                internal_storage="Standard",
                min_price=0,
                max_price=0,
            )
