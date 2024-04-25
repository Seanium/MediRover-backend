from database import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """
    用户

    id: 用户id
    username: 用户名
    password_hash: 密码的哈希值
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password_hash = db.column(db.String(128))

    def set_password(self, password):
        """
        设置密码

        将生成的密码保持到对应字段
        """
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        """
        用于验证密码的方法，接受密码作为参数

        返回布尔值，表示密码是否正确
        """
        return check_password_hash(self.password_hash, password)
