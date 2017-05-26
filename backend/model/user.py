from run import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(64))
    # 加密密码
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)
    # 验证密码
    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)
    # 生成token，并设置过期时间
    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})
    # 静态的验证token的方法
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # token过期
        except BadSignature:
            return None    # token无效
        user = User.query.get(data['id'])
        return user
