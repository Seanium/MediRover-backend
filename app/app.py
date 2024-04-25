from flask import Flask
from flask_cors import CORS
from flask_json import FlaskJSON
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
# 配置数据库
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "data.sqlite"
)
db.init_app(app)
