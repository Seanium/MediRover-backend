import sys
import os

# 获取当前文件的绝对路径
basedir = os.path.abspath(os.path.dirname(__file__))
# 将当前目录添加到环境变量
sys.path.append(basedir)

from flask import request, Flask
from flask_cors import CORS
import json
from flask_json import FlaskJSON
from flask_sqlalchemy import SQLAlchemy
from views import ros_views
# from models import user_model


# 创建app
app = Flask(__name__)
# 跨域
CORS(app, supports_credentials=True)
# json
FlaskJSON(app)

# 数据库
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "data.sqlite"
)
db = SQLAlchemy(app)


# 类型转换或返回默认值
def get_req_value(key: str, target_type: str, from_data: bool = True):
    if from_data:
        data = json.loads(request.data)
        if target_type == "int":
            if data.get(key, None) is not None and data[key] != "":
                return int(data[key])
            else:
                return 0
        if target_type == "float":
            if data.get(key, None) is not None and data[key] != "":
                return float(data[key])
            else:
                return 0.0
        if target_type == "str":
            if (
                data.get(key, None) is not None
                and data[key] != ""
                and data[key] != '""'
                and data[key] != "''"
            ):
                return data[key]
            else:
                return ""
        if target_type == "order":
            if data.get(key, None) is not None and data[key] != "":
                return tuple(data[key].split(","))
            else:
                return ()
    else:
        if target_type == "int":
            if request.args.get(key) is not None and request.args.get(key) != "":
                return int(request.args.get(key))
            else:
                return 0
        if target_type == "float":
            if request.args.get(key) is not None and request.args.get(key) != "":
                return float(request.args.get(key))
            else:
                return 0.0
        if target_type == "str":
            if (
                request.args.get(key) is not None
                and request.args.get(key) != ""
                and request.args.get(key) != '""'
                and request.args.get(key) != "''"
            ):
                return request.args.get(key)
            else:
                return ""
        if target_type == "order":
            if request.args.get(key) is not None and request.args.get(key) != "":
                return tuple(request.args.get(key).split(","))
            else:
                return ()


# 注册蓝图
app.register_blueprint(ros_views.ros_bp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
