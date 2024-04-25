from database import db
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import time
from app import app
from app import basic_auth, token_auth
from flask import g


class User(db.Model):
    """
    用户

    id: 用户id
    username: 用户名
    password_hash: 密码的哈希值
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default="user")

    def hash_password(self, password):
        """
        用于生成密码哈希值的方法，接受密码作为参数
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        用于验证密码的方法，接受密码作为参数

        返回布尔值，表示密码是否正确
        """
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in=600):
        """
        生成认证 token

        expires_in: token 的有效时间
        """
        return jwt.encode(
            {"id": self.id, "exp": time.time() + expires_in},
            app.config["SECRET_KEY"],
            algorithm="HS256",
        )

    @staticmethod
    def verify_auth_token(token):
        """
        验证 token

        token: 需要验证的 token
        """
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        except:
            return
        return User.query.get(data["id"])


@basic_auth.verify_password
def verify_password(username, password):
    """
    验证密码

    username: 用户名
    password: 密码
    """
    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    # 保存当前登录用户
    g.user = user
    return True


@token_auth.verify_token
def verify_token(token):
    """
    验证 token

    token: token
    """
    user = User.verify_auth_token(token)
    if not user:
        return False
    # 保存当前登录用户
    g.user = user
    return True


@basic_auth.get_user_roles
def get_user_roles(authorization):
    """
    获取用户角色

    authorization: werkzeug.datastructures.auth.Authorization 对象
    """
    username = authorization.username
    user = User.query.filter_by(username=username).first()
    if user is None:
        return []
    return [user.role]


@token_auth.get_user_roles
def get_user_roles(authorization):
    """
    获取用户角色

    authorization: werkzeug.datastructures.auth.Authorization 对象
    """
    token = authorization.token
    user = User.verify_auth_token(token)
    if user is None:
        return []
    return [user.role]
