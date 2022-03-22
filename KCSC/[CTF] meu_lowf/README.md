Khi vào chall thì được 1 cái form điền các thông tin để gửi cho admin.

Điền linh tinh thì nó hiện:

![image](https://user-images.githubusercontent.com/96786536/159389504-7940a77a-ad27-4e4f-bc9b-213f562b62bf.png)

Thấy chả có gì nên mình sử dụng dirsearch xem có gì không

Thì được như sau:

![image](https://user-images.githubusercontent.com/96786536/159389692-cd749957-b4f5-471c-8abc-759bd94f0cc0.png)

Truy cập vào `index.pHp` có source như sau:

```php
<?php
	namespace PHPMailer;
	include "PHPMailer/PHPMailer/src/PHPMailer.php";
	
	$check = isset($_POST["fname"]) && isset($_POST["email"]) && isset($_POST["country"]) && isset($_POST["subject"]);
	$check2 = empty($_POST["fname"]) || empty($_POST["email"]) || empty($_POST["country"]) || empty($_POST["subject"]);

	if ($check && !$check2){

		$fullname = $_POST["fname"];
		$email = $_POST["email"];
		$country = $_POST["country"];
		$subject = $_POST["subject"];
		$type = "";
		if (isset($_GET["type"])){
			$type = $_GET["type"];
		}

		
		$is_valid_email = PHPMailer\PHPMailer::validateAddress($email,$type);
			if($is_valid_email!==True){
			$resp = "<script>alert('Oh no wrong email!\\n ErroR:".$is_valid_email."');</script>";
		}
		else{
			$resp = "Do mÃ¬nh lÆ°á»i nÃªn khÃ´ng code ná»¯a Ä‘Ã¢u :( ";
		}

	}
?>

<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body {font-family: Arial, Helvetica, sans-serif;}
* {box-sizing: border-box;}

input[type=text], select, textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
  margin-top: 6px;
  margin-bottom: 16px;
  resize: vertical;
}

input[type=submit] {
  background-color: #04AA6D;
  color: white;
  padding: 12px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

input[type=submit]:hover {
  background-color: #45a049;
}

.container {
  border-radius: 5px;
  background-color: #f2f2f2;
  padding: 20px;
}
</style>
</head>
<body>

<h3>Contact Form</h3>

<div class="container">
  <form action="" method="POST">
    <label for="fname">First Name</label>
    <input type="text" id="fname" name="fname" placeholder="Your name.." required="">

    <label for="email">Email</label>
    <input type="text" id="email" name="email" placeholder="Your email.." required="">

    <label for="country">Country</label>
    <select id="country" name="country">
      <option value="VietNam">VietNam</option>
      <option value="KCSC">KCSC</option>
    </select>

    <label for="subject">Subject</label>
    <textarea id="subject" name="subject" placeholder="Write something.." style="height:200px" required=""></textarea>

    <input type="submit" value="Submit">
  </form>
</div>
<?php if(isset($resp)){echo "<b style=\"background-color: red;color: white;\">$resp</b>";}?>
</body>
</html>
```
