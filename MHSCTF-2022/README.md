# James Harold Japp 

 Đề bài:
 
![image](https://user-images.githubusercontent.com/96786536/154807874-115fef60-7552-41af-98d8-70caeeaa62fd.png)

Có nghĩa là mình làm sao để đăng nhập vào được là được:

Vào trang thì thấy có phần nhập pass để Login, check `source` thấy có 1 đoạn `JS` check value password, nếu giá trị của password là `this_is_a_really_secure_password` thì sẽ chuyển sang trang `/weirdpage.php?pwd=doublepassword`.
`source check pass`:
```js
    <script>
      function validatepwd() {
        var x = document.getElementById("pwd").value;
        if (x == "this_is_a_really_secure_password") {
          window.open("/weirdpage.php?pwd=doublepassword")
        }
      }
    </script>
 ```

Mình đã thử nhập và được thông báo là trang không tồn tại, cứ nghĩ là sai nhưng khi check `source` của trang đó thì được flag.

FLAG: `flag{1n$p3ct0r_g3n3r@l}`

# new site who dis?

Đề bài:

![image](https://user-images.githubusercontent.com/96786536/154808084-ab5d1005-21cf-45af-be12-a8454aabde50.png)

Khi mình truy cập vào trang thì thấy có dòng `Admins, get your flag here!`, nhấp vào thì hiện dòng chữ phải là `admin` thì mới xem được `super-secret flag`.

Đến đây thì mình nghi là bài này liên quan đến `Cookie` vì không thấy có phần Login hay cái gì đó liên quan để truy cập quyền `admin`, mình check cookie thấy có `user=basic`, sửa lại thanh `user=admin` thế là có flag.

FLAG: `flag{1t$-@_m3_Mari0}`

# Bend

Đề bài:

![image](https://user-images.githubusercontent.com/96786536/154808353-60bbde60-848e-430d-9403-3cbd60f7e93e.png)

Sau khi truy cập vào web và vào click `here` để vào `/flag` thì bị chuyển sang video rickroll :).

Thấy không ổn nên bật `Burp suite` lên để chặn request `/flag` xem có gì không thì có flag thật:

FLAG: `flag{g3t_cur1ed}`

# Piece It Together

Đề bài:

![image](https://user-images.githubusercontent.com/96786536/154810281-959baa7d-a63d-4a0b-8021-78c3d25f141e.png)

Đọc đầu bài thì bài này có vẻ là source đã bị mã hóa.

Xem source thì đúng như vậy, code có vẻ rất loằng ngoằng, rồi tra Google xem đây là loại mã hóa gì thì chả thấy gì, Ngại không tìm nữa, nghĩ cách khác, chúng ta có thể sử dụng hàm toString để đọc được hàm `checkpwd()` dưới dạng String.

Có code của hàm `checkpwd()` rồi tìm tiếp array `_0xa8fe` vì mình thấy hàm `checkpwd` có liên quan đến mảng này. Lọ mọ mãi rồi cũng ra được flag:

![image](https://user-images.githubusercontent.com/96786536/154810514-97a5e102-877e-40cc-b61d-82d5016fdf99.png)

FLAG: `flag{j1gs4w}`

# Cuppa Joe

Đề bài:

![image](https://user-images.githubusercontent.com/96786536/154808584-6e1a6a91-e695-4f5f-8661-4d5e0e41e0ca.png)

Vào chal đã thấy giống bị `XSS` rồi, và nó bị thật.

Giờ chỉ việc tìm script để đọc file `flag.php` thôi, sau khi hỏi anh cả Google thì được script:

```js
 <script>
 x=new XMLHttpRequest;
 x.onload=function(){document.write(this.responseText)};
 x.open("GET","flag.php");x.send();
 </script> 
 ```
 
 Ròi chỉ việc gửi script cà lấy flag thôi.
 
 FLAG: `flag{c0ff33_be4nz}`
 
 # Erlenmeyer Biscuits (Cuppa Joe 2)
 
 Đề bài:
 
 ![image](https://user-images.githubusercontent.com/96786536/154808742-15bf8cdc-266a-4008-8d3c-ae525b05d222.png)

Đọc đầu bài thì có vẻ lại liên quan đến Cookie thì phải, check thử thì thấy có Cookie: `session=eyJmbGFnIjoiZmxhZ3tmbDQ1a19zMzU1MTBuX2MwMGsxM3NfNHIzXzFuNTNjdXJlfSJ9.YFLMhA.xt_8C0BrPHl2HDm9yIRffDhK7Ow`. Trông có vẻ giống `JWT`.

Thử mang đi decode base 64 xem được gì thì được luôn flag :)).

FLAG: `flag{fl45k_s35510n_c00k13s_4r3_1n53cure}`

# Et tu, Brute?

Đề bài:

![image](https://user-images.githubusercontent.com/96786536/154808874-230a7b0d-d46a-4961-8082-d2b5fd7e9794.png)

Nghe tên đầu bài đã thấy có mùi brute force rồi :)).

Vào chall thì có vẻ đúng như vậy.

Nhập 2 số từ 1 đến 100 nếu trùng với `Favorite Number` thì có flag.

Mình ngại viết script nên dùng Burp Suite.

Sau 2 phút chạy thì cũng ra được flag:

FLAG: `flag{pur3_s7r3ngth}`

# Practice For School

Đề bài:

![image](https://user-images.githubusercontent.com/96786536/154809233-57512d49-d2ad-4364-8449-73b3f1ab5be6.png)

Đây là bài làm mình tốn nhiều thời gian nhất vì đi sai hướng.

Đầu tiên mình không để ý tên URL, sau khi để ý thì thấy URL này không giống với các URL của bài khác, tra google thì mới biết được đấy là một trang học tập giống kiểu Kahoot hay Quizz,... Mình tra google xem có cheat nào để tăng tốc video hay bỏ qua video không, sau một hồi thử tăng speed video lên thì cũng có vẻ không khả thi, quay ra tìm cách bỏ qua video, mình đã làm thử theo video này và đã lấy được flag: `https://www.youtube.com/watch?v=8KP-CmZSm_w`

FLAG: `flag{th1s_15_a_us3ful_expl0it_f0r_sch00l}`
