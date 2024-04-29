import sys
import os

# 添加父目录到系统路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

# 打印系统路径
print(sys.path)

from app import app
from database import db
from views.ros_views import ros_bp
from views.user_views import user_bp
from views.map_views import map_bp
from views.waypoint_views import waypoint_bp
from views.robot_views import robot_bp
from views.rx_views import rx_bp
from views.pt_views import pt_bp
import click

# 注册蓝图
app.register_blueprint(ros_bp)
app.register_blueprint(user_bp)
app.register_blueprint(map_bp)
app.register_blueprint(waypoint_bp)
app.register_blueprint(robot_bp)
app.register_blueprint(rx_bp)
app.register_blueprint(pt_bp)
app.config["SECRET_KEY"] = "the quick brown fox jumps over the lazy dog"


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
    # 获取当前文件所属目录的绝对路径
    basedir = os.path.abspath(os.path.dirname(__file__))
    if not os.path.exists(os.path.join(basedir, "data.sqlite")):
        with app.app_context():
            db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
