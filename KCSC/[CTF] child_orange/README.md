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
