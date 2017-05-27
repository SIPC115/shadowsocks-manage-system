# coding:utf-8
import json
import os

from flask import Flask, abort, g, jsonify, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth
import flask_login

from models.database.database import db_session
from models.user import User

app = Flask(__name__)
app.secret_key = 'debudedebude  # Change this!
# app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
# app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://sipc115:sipc115@127.0.0.1:3306/shadowsocks_manage'
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

auth = HTTPBasicAuth()

def init_db():
    import models
    from models.database.database import Base, engine
    Base.metadata.create_all(bind=engine)

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
    db_session.add(user)
    db_session.commit()
    # 成功注册后返回用户名，Location后面接着的是跳转的地址
    return jsonify({'username': user.username})

@app.route('/login')
@auth.login_required
def _login():
    token = g.user.generate_auth_token(600)
    resp = make_response(jsonify({'token': token.decode('ascii'), 'duration': 600}))
    resp.set_cookie('user', token)
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0')
