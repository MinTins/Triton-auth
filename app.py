from flask import Flask, render_template, request, make_response
from triton import triton_auth

app = Flask(__name__)


TRITON_TOKEN_NAME = "tc"


@app.route('/')
def index():
    if TRITON_TOKEN_NAME in request.args:
        token = request.args[TRITON_TOKEN_NAME]
        resp = make_response(render_template('login.html'))
        resp.set_cookie(TRITON_TOKEN_NAME, token)
        return resp
    else:
        return render_template('login.html')


# change for your needs
def success_auth(token, res):
    print(token)


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    res = triton_auth(username, password)
    if res is not None:
        token = request.cookies.get(TRITON_TOKEN_NAME)
        success_auth(token, res)

        return render_template("success.html", res=res)
    else:
        return render_template("error.html"),401

if __name__ == '__main__':
    app.run(debug=True)