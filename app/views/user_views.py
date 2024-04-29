from flask import Blueprint, g
from models.user_model import User
from flask_json import JsonError, json_response, request
from database import db
from app import multi_auth

user_bp = Blueprint("user_views", __name__)


@user_bp.route("/users", methods=["POST"])
def new_user():
    """
    注册新用户
    请求体必须包含一个定义了用户名和密码字段的 JSON 对象，也可以包含一个可选的角色字段。
    成功时，返回状态码 201。响应体包含一个 JSON 对象，其中包含新添加的用户的信息。
    失败时，返回状态码 400（请求错误）。
    ---
    tags:
      - User
    parameters:
      - in: body
        name: body
        schema:
          id: User
          required:
            - username
            - password
          properties:
            username:
              type: string
              description: 用户名
            password:
              type: string
              description: 密码
            role:
              type: string
              description: 用户角色
    responses:
      200:
        description: 用户创建成功
        schema:
          id: UserResponse
          properties:
            id:
              type: integer
              description: 用户 ID
            username:
              type: string
              description: 用户名
            role:
              type: string
              description: 用户角色
            message:
              type: string
              description: 返回消息
      400:
        description: 请求错误，可能的原因包括用户名和密码不能为空，或用户名已存在
    """
    username = request.json.get("username")
    password = request.json.get("password")
    role = request.json.get("role", "user")  # 如果未提供角色，设置为 "user"
    if username is None or password is None:
        # 返回错误：用户名和密码不能为空
        raise JsonError(description="用户名和密码不能为空")
    if User.query.filter_by(username=username).first() is not None:
        # 返回错误：用户名为 {username} 的用户已存在
        raise JsonError(description=f"用户名为 {username} 的用户已存在")
    user = User(username=username, role=role)  # 在创建用户时设置角色
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return json_response(
        id=user.id, username=user.username, role=user.role, message="用户创建成功"
    )


@user_bp.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    """
    获取用户信息
    成功时，返回状态码 200。响应体包含一个 JSON 对象，其中包含请求的用户信息。
    失败时，返回状态码 400（请求错误）。
    ---
    tags:
      - User
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: 用户 ID
    responses:
      200:
        description: 用户信息
        schema:
          id: UserResponse
          properties:
            id:
              type: integer
              description: 用户 ID
            username:
              type: string
              description: 用户名
            role:
              type: string
              description: 用户角色
      400:
        description: 请求错误，可能的原因包括不存在 ID 为 {id} 的用户
    """
    user = User.query.get(id)
    if not user:
        # 返回错误：不存在id为 {id} 的用户
        raise JsonError(description=f"不存在id为 {id} 的用户")
    return json_response(id=user.id, username=user.username, role=user.role)


@user_bp.route("/token", methods=["GET"])
@multi_auth.login_required
def get_auth_token():
    """
    获取授权令牌
    此请求可以使用HTTP Basic Auth（提供用户名和密码）或者 Bearer Token（请求头 Authorization: Bearer {token}）进行认证。
    成功时，返回一个 JSON 对象，其中包含一个 token 字段，设置为用户的认证令牌，和一个 duration 字段，设置为令牌有效的秒数。
    失败时，返回状态码 401（未授权）。
    ---
    tags:
      - User
    responses:
      200:
        description: 授权令牌和有效期
        schema:
          id: AuthTokenResponse
          properties:
            token:
              type: string
              description: 授权令牌
            duration:
              type: integer
              description: 有效期（秒）
    security:
      - ApiKeyAuth: []
    """
    token = g.user.generate_auth_token(600)
    return json_response(token=token, duration=600)


@user_bp.route("/users/password", methods=["PUT"])
@multi_auth.login_required
def change_password():
    """
    修改当前登录用户的密码
    ---
    tags:
      - User
    parameters:
      - in: body
        name: body
        schema:
          id: PasswordChange
          required:
            - old_password
            - new_password
          properties:
            old_password:
              type: string
              description: 旧密码
            new_password:
              type: string
              description: 新密码
    responses:
      200:
        description: 密码修改成功
        schema:
          id: PasswordChangeResponse
          properties:
            message:
              type: string
              description: 返回消息
      400:
        description: 请求错误，可能的原因包括旧密码不正确，新密码不符合要求等
    security:
      - Bearer: []
    """
    user = g.user
    old_password = request.json.get("old_password")
    new_password = request.json.get("new_password")

    if not user.verify_password(old_password):
        # 返回错误：旧密码不正确
        raise JsonError(description="旧密码不正确")

    # if not new_password or len(new_password) < 8:
    #     # 返回错误：新密码不符合要求
    #     raise JsonError(description="新密码不符合要求，必须至少包含8个字符")

    user.hash_password(new_password)
    db.session.commit()

    return json_response(message="密码修改成功")


@user_bp.route("/test_public", methods=["GET"])
def get_public_resource():
    """
    获取公开资源（测试用）
    ---
    tags:
      - User
    responses:
      200:
        description: 公开资源数据
        schema:
          id: PublicResourceResponse
          properties:
            data:
              type: string
              description: 公开资源数据
    """
    return json_response(data="Hello, public!")


@user_bp.route("/test_login", methods=["GET"])
@multi_auth.login_required
def get_resource():
    """
    登录状态获取资源（测试用）
    ---
    tags:
      - User
    security:
      - Bearer: []
    responses:
      200:
        description: 用户获取的资源数据
        schema:
          id: UserResourceResponse
          properties:
            data:
              type: string
              description: 用户获取的资源数据
    """
    return json_response(data="Hello, %s!" % g.user.username)


@user_bp.route("/test_admin", methods=["GET"])
@multi_auth.login_required(role="admin")
def get_admin_resource():
    """
    管理员获取资源（测试用）
    ---
    tags:
      - Admin
    security:
      - Bearer: []
    responses:
      200:
        description: 管理员获取的资源数据
        schema:
          id: AdminResourceResponse
          properties:
            data:
              type: string
              description: 管理员获取的资源数据
    """
    return json_response(data="Hello, admin %s!" % g.user.username)
