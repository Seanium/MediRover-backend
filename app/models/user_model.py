from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """
    用户

    id: 用户id
    username: 用户名
    password_hash: 哈希处理后的密码
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password_hash = db.column(db.String(128))

    def set_password(self, password):
        """
        设置密码
        """
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        """
        验证密码
        """
        return check_password_hash(self.password_hash, password)
