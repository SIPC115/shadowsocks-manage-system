# coding:utf-8
from sqlalchemy import Column, Integer, String
from database.database import Base
from passlib.apps import custom_app_context as pwd_context
from flask_login import UserMixin

class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), index=True)
    password_hash = Column(String(128))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    # def generate_auth_token(self, expiration=600):
    #     s = Serializer(SECRET_KEY, expires_in=expiration)
    #     return s.dumps({'id': self.id})

    # @staticmethod
    # def verify_auth_token(token):
    #     s = Serializer(SECRET_KEY)
    #     try:
    #         data = s.loads(token)
    #     except SignatureExpired:
    #         return None
    #     except BadSignature:
    #         return None
    #     user = User.query.get(data['id'])
    #     return user
        def is_authenticated(self):
            return True

        def is_actice(self):
            return True

        def is_anonymous(self):
            return False

        def get_id(self):
            return self.id
