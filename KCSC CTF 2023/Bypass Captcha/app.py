from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def get_user():
    user = {
        "success": True,
        "challenge_ts": "2024-02-28T15:14:30.096Z",
        "hostname": "example.com",
        "error-codes": [],
        "action": "login",
        "cdata": "sessionid-123456789"
    }
    return jsonify(user)

if __name__ == '__main__':
    app.run()
