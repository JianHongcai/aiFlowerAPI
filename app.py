from flask import Flask, request
from database import dataBaseManager

app = Flask(__name__)

c = dataBaseManager()


@app.route('/register', methods=["POST"])
def register():
    data = request.get_json()
    if c.user_exists(data['account']) is not None:
        return {"message": "账户已被注册","code":400}, 400
    else:
        return c.register(password=data['password'], account=data['account'])


@app.route('/login', methods=["POST"])
def login():
    data = request.get_json()
    if c.user_exists(data['account']) is None:
        return {"message": "账户未注册，请先注册账户后再登陆!","code":400}, 400
    else:
        return c.login(data['account'], data['password'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
