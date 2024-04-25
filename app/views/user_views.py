from flask import Blueprint
from models.user_model import User
from flask_json import JsonError, json_response

user_bp = Blueprint("user_views", __name__)


@user_bp.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get(id)
    if not user:
        # 输出“不存在id为 {id} 的用户”错误
        raise JsonError(description=f"不存在id为 {id} 的用户")
    return json_response(id=user.id, username=user.username)
