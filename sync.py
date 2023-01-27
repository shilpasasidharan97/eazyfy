import requests
from bs4 import BeautifulSoup


items = []


def get_data(url, brand_slug, brand_pk):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    start_number = 208
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
                "pk": start_number,
                "fields": {
                    "brand": brand_pk,
                    "image": image,
                    "name": name,
                    "slug": name.lower().replace(" ", "-"),
                    "description": description,
                    "is_mostselling": 0,
                    # "photo_url": photo_url,
                },
            }
        )
        start_number += 1
    return items


data = [
    {
        "brand_slug": "acer",
        "brand_pk": 26,
        "urls": [
            "https://www.gsmarena.com/acer-phones-59.php",
            "https://www.gsmarena.com/acer-phones-f-59-0-p2.php",
            "https://www.gsmarena.com/acer-phones-f-59-0-p3.php",
        ],
    }
]

final = []
for url in data:
    for u in url["urls"]:
        final += get_data(u, url["brand_slug"], url["brand_pk"])


# convert to json file
import json

with open("hello.json", "w") as f:
    json.dump(final, f, indent=4)
