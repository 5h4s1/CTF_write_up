
`Natas level 2`:

Chall này thì vào không thấy có hướng dẫn gì nữa, check source thì thấy file ảnh PNG được lấy từ folder files. Check folder files có được file `users.txt`, vào thì có pass của chall tiếp:

![image](https://user-images.githubusercontent.com/96786536/147645060-674519ce-408f-4bcc-85f5-2de5e48d350c.png)

`Natas level 3`:

Tiếp tục 1 chall ko có hint gì cà :). Check thử thì thấy tệp robots truy cập được:

![image](https://user-images.githubusercontent.com/96786536/147678329-d26f2a50-b51a-477d-96c0-367ce19ef7cc.png)

tiếp tục vào /s3cr3t/ thì được pass:

![image](https://user-images.githubusercontent.com/96786536/147678391-e31dfc68-4cd6-4fc7-9adc-b82aa58fb7c6.png)


`Natas level 4`:

Khi vào trong thì được thông báo như vậy:

![image](https://user-images.githubusercontent.com/96786536/147679350-3eb102d4-5110-4302-a235-18869400bb0b.png)

có nghía là trang web chỉ chấp nhận các truy cập từ url : `http://natas5.natas.labs.overthewire.org/`. Chúng ra dùng Burp suite để bắt request rồi sau đso thay đôie header để access url:

![image](https://user-images.githubusercontent.com/96786536/147679572-87854c7e-a3f2-4f89-8d58-8174c3cca628.png)


Chỉ cần sửa Header `Referer` thành url mà web yêu cầu là có pass.

`Natas level 5`:

![image](https://user-images.githubusercontent.com/96786536/147680018-2990c82a-4068-414a-b5b5-f924664a78e6.png)

web yêu cầu mình đăng nhập vào thì mới được, mà mình không thấy chỗ đăng nhập ở đâu nên nghĩ có lẽ là liên quan đến cookie.

![image](https://user-images.githubusercontent.com/96786536/147680189-127fa352-24a0-4c6f-9e19-322f6e1e24e5.png)

đúng như vậy, có cookie tên loggedin=0, chỉ cần sửa giá trị thành 1 là đc:

![image](https://user-images.githubusercontent.com/96786536/147680284-1bc280d1-1587-44d0-b35d-b29cd31af2d5.png)

Vậy là có pass.

`Natas level 6`:
 Vào web thì có source:
 ```php
 <html>
<head>
<!-- This stuff in the header has nothing to do with the level -->
<link rel="stylesheet" type="text/css" href="http://natas.labs.overthewire.org/css/level.css">
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/jquery-ui.css" />
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/wechall.css" />
<script src="http://natas.labs.overthewire.org/js/jquery-1.9.1.js"></script>
<script src="http://natas.labs.overthewire.org/js/jquery-ui.js"></script>
<script src=http://natas.labs.overthewire.org/js/wechall-data.js></script><script src="http://natas.labs.overthewire.org/js/wechall.js"></script>
<script>var wechallinfo = { "level": "natas6", "pass": "<censored>" };</script></head>
<body>
<h1>natas6</h1>
<div id="content">

<?

include "includes/secret.inc";

    if(array_key_exists("submit", $_POST)) {
        if($secret == $_POST['secret']) {
        print "Access granted. The password for natas7 is <censored>";
    } else {
        print "Wrong secret";
    }
    }
?>

<form method=post>
Input secret: <input name=secret><br>
<input type=submit name=submit>
</form>

<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>
```
thấy code có include "includes/secret.inc", truy cập vào đó là có secret:

![image](https://user-images.githubusercontent.com/96786536/148688758-43c45e4a-6195-4c6b-8822-abbfa8524877.png)

lụm pass thôi :)

`Natas level 7`:

![image](https://user-images.githubusercontent.com/96786536/148688811-e46fddad-3839-49a1-9600-df495dbe6b8d.png)

nhìn url nghi nghi là LFI rồi, check source thì có hint, rồi thay `/etc/natas_webpass/natas8` vào url là có pass thôi:

![image](https://user-images.githubusercontent.com/96786536/148688874-fc826194-fcc1-41c1-af57-e0827bb7e807.png)

`Natas level 8`:

Source:

```php
 <html>
<head>
<!-- This stuff in the header has nothing to do with the level -->
<link rel="stylesheet" type="text/css" href="http://natas.labs.overthewire.org/css/level.css">
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/jquery-ui.css" />
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/wechall.css" />
<script src="http://natas.labs.overthewire.org/js/jquery-1.9.1.js"></script>
<script src="http://natas.labs.overthewire.org/js/jquery-ui.js"></script>
<script src=http://natas.labs.overthewire.org/js/wechall-data.js></script><script src="http://natas.labs.overthewire.org/js/wechall.js"></script>
<script>var wechallinfo = { "level": "natas8", "pass": "<censored>" };</script></head>
<body>
<h1>natas8</h1>
<div id="content">

<?

$encodedSecret = "3d3d516343746d4d6d6c315669563362";

function encodeSecret($secret) {
    return bin2hex(strrev(base64_encode($secret)));
}

if(array_key_exists("submit", $_POST)) {
    if(encodeSecret($_POST['secret']) == $encodedSecret) {
    print "Access granted. The password for natas9 is <censored>";
    } else {
    print "Wrong secret";
    }
}
?>

<form method=post>
Input secret: <input name=secret><br>
<input type=submit name=submit>
</form>

<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>
```
Chú ý vào function `encodeSecret`, dịch ngược lại là có secret:

![image](https://user-images.githubusercontent.com/96786536/148689206-8f62255c-f4a9-4ce2-b62d-8d8cbd25f028.png)

`Natas level 9:`

Source:

```php
 <html>
<head>
<!-- This stuff in the header has nothing to do with the level -->
<link rel="stylesheet" type="text/css" href="http://natas.labs.overthewire.org/css/level.css">
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/jquery-ui.css" />
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/wechall.css" />
<script src="http://natas.labs.overthewire.org/js/jquery-1.9.1.js"></script>
<script src="http://natas.labs.overthewire.org/js/jquery-ui.js"></script>
<script src=http://natas.labs.overthewire.org/js/wechall-data.js></script><script src="http://natas.labs.overthewire.org/js/wechall.js"></script>
<script>var wechallinfo = { "level": "natas9", "pass": "<censored>" };</script></head>
<body>
<h1>natas9</h1>
<div id="content">
<form>
Find words containing: <input name=needle><input type=submit name=submit value=Search><br><br>
</form>


Output:
<pre>
<?
$key = "";

if(array_key_exists("needle", $_REQUEST)) {
    $key = $_REQUEST["needle"];
}

if($key != "") {
    passthru("grep -i $key dictionary.txt");
}
?>
</pre>

<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>

```
Đây là bài command injection.
Payload: `; cat /etc/natas_webpass/natas10`, có nghĩa là dấu ; sẽ kết thúc một dòng command, viết thêm gì đằng sau đó sẽ là command mới.
Pass: nOpp1igQAkUzaI1GUUjzn1bFVj7xCNzu.

`Natas level 10:`

Source:

```php
 <html>
<head>
<!-- This stuff in the header has nothing to do with the level -->
<link rel="stylesheet" type="text/css" href="http://natas.labs.overthewire.org/css/level.css">
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/jquery-ui.css" />
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/wechall.css" />
<script src="http://natas.labs.overthewire.org/js/jquery-1.9.1.js"></script>
<script src="http://natas.labs.overthewire.org/js/jquery-ui.js"></script>
<script src=http://natas.labs.overthewire.org/js/wechall-data.js></script><script src="http://natas.labs.overthewire.org/js/wechall.js"></script>
<script>var wechallinfo = { "level": "natas10", "pass": "<censored>" };</script></head>
<body>
<h1>natas10</h1>
<div id="content">

For security reasons, we now filter on certain characters<br/><br/>
<form>
Find words containing: <input name=needle><input type=submit name=submit value=Search><br><br>
</form>


Output:
<pre>
<?
$key = "";

if(array_key_exists("needle", $_REQUEST)) {
    $key = $_REQUEST["needle"];
}

if($key != "") {
    if(preg_match('/[;|&]/',$key)) {
        print "Input contains an illegal character!";
    } else {
        passthru("grep -i $key dictionary.txt");
    }
}
?>
</pre>

<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>
```
Cũng vẫn là command injection nhưng bị filter r:
Payload: `1 /etc/natas_webpass/natas11`. Giải thích chút là lệnh grep sẽ tìm kí tự '1' trong file /etc/natas_webpass/natas11 và dictionary.txt.
Password: U82q5TCMMQ9xuFoI3dYX61s7OZD9JKoK

`Natas level 11:`

