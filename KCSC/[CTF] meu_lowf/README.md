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


```

Nhìn source thì không có gì quan tâm nhiều, chỉ có quan tâm đến `$_POST["email"]` và `$_GET["type"]` vì đây là hai tham số được truyền vào `PHPMailer\PHPMailer::validateAddress($email,$type)`.

Rồi chúng ta đi vào hàm `validateAddress` xem nó có gì. Hàm `validateAddress` sẽ ở file `http://localhost:1020/phpmailer/PHPMailer/src/PHPMailer.pHp`.

Function `validateAddress`:

```php
public static function validateAddress($address, $patternselect = null)
    {
        if (null === $patternselect) {
            $patternselect = static::$validator; // php
        }
        if (is_callable($patternselect)) {
            return call_user_func($patternselect, $address);
        }
        //Reject line breaks in addresses; it's valid RFC5322, but not RFC5321
        if (strpos($address, "\n") !== false || strpos($address, "\r") !== false) {
            return false;
        }
        switch ($patternselect) {
            case 'pcre': //Kept for BC
            case 'pcre8':
                /*
                 * A more complex and more permissive version of the RFC5322 regex on which FILTER_VALIDATE_EMAIL
                 * is based.
                 * In addition to the addresses allowed by filter_var, also permits:
                 *  * dotless domains: `a@b`
                 *  * comments: `1234 @ local(blah) .machine .example`
                 *  * quoted elements: `'"test blah"@example.org'`
                 *  * numeric TLDs: `a@b.123`
                 *  * unbracketed IPv4 literals: `a@192.168.0.1`
                 *  * IPv6 literals: 'first.last@[IPv6:a1::]'
                 * Not all of these will necessarily work for sending!
                 *
                 * @see       http://squiloople.com/2009/12/20/email-address-validation/
                 * @copyright 2009-2010 Michael Rushton
                 * Feel free to use and redistribute this code. But please keep this copyright notice.
                 */
                return (bool) preg_match(
                    '/^(?!(?>(?1)"?(?>\\\[ -~]|[^"])"?(?1)){255,})(?!(?>(?1)"?(?>\\\[ -~]|[^"])"?(?1)){65,}@)' .
                    '((?>(?>(?>((?>(?>(?>\x0D\x0A)?[\t ])+|(?>[\t ]*\x0D\x0A)?[\t ]+)?)(\((?>(?2)' .
                    '(?>[\x01-\x08\x0B\x0C\x0E-\'*-\[\]-\x7F]|\\\[\x00-\x7F]|(?3)))*(?2)\)))+(?2))|(?2))?)' .
                    '([!#-\'*+\/-9=?^-~-]+|"(?>(?2)(?>[\x01-\x08\x0B\x0C\x0E-!#-\[\]-\x7F]|\\\[\x00-\x7F]))*' .
                    '(?2)")(?>(?1)\.(?1)(?4))*(?1)@(?!(?1)[a-z0-9-]{64,})(?1)(?>([a-z0-9](?>[a-z0-9-]*[a-z0-9])?)' .
                    '(?>(?1)\.(?!(?1)[a-z0-9-]{64,})(?1)(?5)){0,126}|\[(?:(?>IPv6:(?>([a-f0-9]{1,4})(?>:(?6)){7}' .
                    '|(?!(?:.*[a-f0-9][:\]]){8,})((?6)(?>:(?6)){0,6})?::(?7)?))|(?>(?>IPv6:(?>(?6)(?>:(?6)){5}:' .
                    '|(?!(?:.*[a-f0-9]:){6,})(?8)?::(?>((?6)(?>:(?6)){0,4}):)?))?(25[0-5]|2[0-4][0-9]|1[0-9]{2}' .
                    '|[1-9]?[0-9])(?>\.(?9)){3}))\])(?1)$/isD',
                    $address
                );
            case 'html5':
                /*
                 * This is the pattern used in the HTML5 spec for validation of 'email' type form input elements.
                 *
                 * @see https://html.spec.whatwg.org/#e-mail-state-(type=email)
                 */
                return (bool) preg_match(
                    '/^[a-zA-Z0-9.!#$%&\'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}' .
                    '[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/sD',
                    $address
                );
            case 'php':
            default:
                return filter_var($address, FILTER_VALIDATE_EMAIL) !== false;
        }
    }
```

Chúng ta để ý đến if thứ hai sẽ gọi hàm `is_callable` để check xem `$patternselect1` có phải là hàm hay phương thức thực hiện được không. Nếu `is_callable` đúng thì sẽ gọi đến hàm `call_user_func` để thực thi hàm `$patternselect` ($_GET["type"]) và tham số là `$address` ($_POST["email"]).

Rồi sau khi đã hiểu và tìm được chỗ có thể khai thác thì chúng ta bắt đầu khai thác:

Thử payload với `$_GET["type"]=system` và `$_POST["email"]=ls` xem có thực thi hàm system được không và được:

![image](https://user-images.githubusercontent.com/96786536/159439991-14e88ea3-a475-4aa2-a1e1-dde198e7bd47.png)

-> RCE thành công. Rồi đọc flag thôi:

![image](https://user-images.githubusercontent.com/96786536/159440124-63bc06b1-aace-4e88-9509-9be45485993f.png)


