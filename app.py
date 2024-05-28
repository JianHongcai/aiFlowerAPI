from flask import Flask, request
from database import dataBaseManager


app = Flask(__name__)

c = dataBaseManager()


@app.route('/<username>', methods=["GET"])
def checkAccout(username):
    return str(c.card_exists(username))


@app.route('/register', methods=["POST"])
def register():
    data = request.get_json()
    print(data)
    return c.register(username=data['username'], password=data['password'], account=data['account'])
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
