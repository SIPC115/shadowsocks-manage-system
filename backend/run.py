# coding:utf-8
import json
import os

from flask import Flask, abort, request, jsonify, g, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth

from user impoer *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://sipc115:sipc115@127.0.0.1:3306/shadowsocks_manage'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True

db = SQLAlchemy(app)

auth = HTTPBasicAuth()

@app.route('/index')
def _index():
    return 'hello flask'

@app.route('/signup', methods=['POST'])
def _signup():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)
    if User.query.filter_by(username=username).first() is not None:
        abort(400)
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    # 成功注册后返回用户名，Location后面接着的是跳转的地址
    return jsonify({'username': user.username})

@app.route('/login')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    resp = make_response(jsonify({'token': token.decode('ascii'), 'duration': 600}))
    resp.set_cookie('user', token)
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0')
