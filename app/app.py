import sys
import os

# 获取当前文件的绝对路径
basedir = os.path.abspath(os.path.dirname(__file__))
# 将当前目录添加到环境变量
sys.path.append(basedir)

from flask import Flask
from flask_cors import CORS
from flask_json import FlaskJSON
from database import db
import click

# 创建 Flask 实例
app = Flask(__name__)
# 跨域
CORS(app, supports_credentials=True)
# json 解析扩展
FlaskJSON(app)
# 配置数据库
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "data.sqlite"
)
db.init_app(app)

# 导入并注册蓝图
# 注意这里是在 create_app 函数中导入，而不是在文件头部导入，避免循环导入
from views import user_views, ros_views

# 注册蓝图
app.register_blueprint(ros_views.ros_bp)
app.register_blueprint(user_views.user_bp)


@app.cli.command()  # 注册为命令，可以传入 name 参数来自定义命令
@click.option("--drop", is_flag=True, help="Create after drop.")  # 设置选项
def initdb(drop):
    """
    命令行执行 flask initdb 命令创建数据库表，使用 --drop 选项删除表后重新创建
    """
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo("Initialized database.")  # 输出提示信息


if __name__ == "__main__":
    if not os.path.exists(os.path.join(basedir, "data.sqlite")):
        with app.app_context():
            db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
