from flask import Flask
from flask_cors import CORS
from flask_json import FlaskJSON
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from database import db
import os

# 获取当前文件的绝对路径
basedir = os.path.abspath(os.path.dirname(__file__))

# 创建 Flask 实例
app = Flask(__name__)

# 跨域
CORS(app, supports_credentials=True)

# json 解析拓展
FlaskJSON(app)

# 数据库
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "data.sqlite"
)
# app.config['SQLALCHEMY_ECHO'] = True
db.init_app(app)

# 身份认证
basic_auth = HTTPBasicAuth()  # 基本认证
token_auth = HTTPTokenAuth("Bearer")  # token 认证
multi_auth = MultiAuth(basic_auth, token_auth)  # 多重认证
