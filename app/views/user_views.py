from flask import Blueprint, g
from models.user_model import User
from flask_json import JsonError, json_response, request
from database import db
from app import multi_auth, basic_auth, token_auth

user_bp = Blueprint("user_views", __name__)


@user_bp.route("/users", methods=["POST"])
def new_user():
    username = request.json.get("username")
    password = request.json.get("password")
    if username is None or password is None:
        # 返回错误：用户名和密码不能为空
        raise JsonError(description="用户名和密码不能为空")
    if User.query.filter_by(username=username).first() is not None:
        # 返回错误：用户名为 {username} 的用户已存在
        raise JsonError(description=f"用户名为 {username} 的用户已存在")
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return json_response(
        id=user.id, username=user.username, role=user.role, message="用户创建成功"
    )


@user_bp.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get(id)
    if not user:
        # 返回错误：不存在id为 {id} 的用户
        raise JsonError(description=f"不存在id为 {id} 的用户")
    return json_response(id=user.id, username=user.username, role=user.role)


@user_bp.route("/token", methods=["GET"])
@multi_auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return json_response(token=token, duration=600)


@user_bp.route("/test_public", methods=["GET"])
def get_public_resource():
    return json_response(data="Hello, public!")


@user_bp.route("/test_login", methods=["GET"])
@multi_auth.login_required
def get_resource():
    return json_response(data="Hello, %s!" % g.user.username)


@user_bp.route("/test_admin", methods=["GET"])
@multi_auth.login_required(role="admin")
def get_admin_resource():
    return json_response(data="Hello, admin %s!" % g.user.username)
