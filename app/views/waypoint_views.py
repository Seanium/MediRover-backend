from flask import Blueprint
from models.waypoint_model import Waypoint
from flask_json import JsonError, json_response, request
from database import db

waypoint_bp = Blueprint("waypoint", __name__)


@waypoint_bp.route("/waypoints", methods=["GET"])
def get_waypoints():
    """
    获取航点列表
    请求成功时，返回状态码 200。响应体包含一个 JSON 对象，其中包含航点列表。
    ---
    tags:
      - Waypoint
    responses:
      200:
        description: 获取航点列表成功
        schema:
          id: WaypointResponse
          properties:
            waypoints:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    description: 航点 ID
                  waypointname:
                    type: string
                    description: 航点名称
                  pos_x:
                    type: float
                    description: 航点 x 坐标
                  pos_y:
                    type: float
                    description: 航点 y 坐标
                  pos_z:
                    type: float
                    description: 航点 z 坐标
                  ori_x:
                    type: float
                    description: 航点 x 方向
                  ori_y:
                    type: float
                    description: 航点 y 方向
                  ori_z:
                    type: float
                    description: 航点 z 方向
                  ori_w:
                    type: float
                    description: 航点 w 方向
                  table_height:
                    type: float
                    description: 航点桌面高度
    """
    waypoints = Waypoint.query.all()
    return json_response(
        waypoints=[
            {
                "id": waypoint.id,
                "waypointname": waypoint.waypointname,
                "pos_x": waypoint.pos_x,
                "pos_y": waypoint.pos_y,
                "pos_z": waypoint.pos_z,
                "ori_x": waypoint.ori_x,
                "ori_y": waypoint.ori_y,
                "ori_z": waypoint.ori_z,
                "ori_w": waypoint.ori_w,
                "table_height": waypoint.table_height,
            }
            for waypoint in waypoints
        ]
    )


@waypoint_bp.route("/waypoints/<int:waypoint_id>", methods=["GET"])
def get_waypoint(waypoint_id):
    """
    获取航点详情
    请求成功时，返回状态码 200。响应体包含一个 JSON 对象，其中包含航点详情。
    ---
    tags:
      - Waypoint
    parameters:
      - in: path
        name: waypoint_id
        type: integer
    responses:
      200:
        description: 获取航点详情成功
        schema:
          id: WaypointDetail
          properties:
            id:
              type: integer
              description: 航点 ID
            waypointname:
              type: string
              description: 航点名称
            pos_x:
              type: float
              description: 航点 x 坐标
            pos_y:
              type: float
              description: 航点 y 坐标
            pos_z:
              type: float
              description: 航点 z 坐标
            ori_x:
              type: float
              description: 航点 x 方向
            ori_y:
              type: float
              description: 航点 y 方向
            ori_z:
              type: float
              description: 航点 z 方向
            ori_w:
              type: float
              description: 航点 w 方向
            table_height:
              type: float
              description: 航点桌面高度
    """
    waypoint = Waypoint.query.get(waypoint_id)
    if waypoint is None:
        raise JsonError(description="Waypoint not found.")
    return json_response(
        id=waypoint.id,
        waypointname=waypoint.waypointname,
        pos_x=waypoint.pos_x,
        pos_y=waypoint.pos_y,
        pos_z=waypoint.pos_z,
        ori_x=waypoint.ori_x,
        ori_y=waypoint.ori_y,
        ori_z=waypoint.ori_z,
        ori_w=waypoint.ori_w,
        table_height=waypoint.table_height,
    )


@waypoint_bp.route("/waypoints", methods=["POST"])
def create_waypoint():
    """
    创建航点
    请求成功时，返回状态码 200。响应体包含一个 JSON 对象，其中包含创建的航点详情。
    ---
    tags:
      - Waypoint
    parameters:
      - in: body
        name: body
        required: true
        schema:
          id: WaypointCreate
          required:
            - waypointname
            - pos_x
            - pos_y
            - pos_z
            - ori_x
            - ori_y
            - ori_z
            - ori_w
            - table_height
          properties:
            waypointname:
              type: string
              description: 航点名称
            pos_x:
              type: float
              description: 航点 x 坐标
            pos_y:
              type: float
              description: 航点 y 坐标
            pos_z:
              type: float
              description: 航点 z 坐标
            ori_x:
              type: float
              description: 航点 x 方向
            ori_y:
              type: float
              description: 航点 y 方向
            ori_z:
              type: float
              description: 航点 z 方向
            ori_w:
              type: float
              description: 航点 w 方向
            table_height:
              type: float
              description: 航点桌面高度
    responses:
      200:
        description: 创建航点成功
        schema:
          id: WaypointDetail
          properties:
            id:
              type: integer
              description: 航点 ID
            waypointname:
              type: string
              description: 航点名称
            pos_x:
              type: float
              description: 航点 x 坐标
            pos_y:
              type: float
              description: 航点 y 坐标
            pos_z:
              type: float
              description: 航点 z 坐标
            ori_x:
              type: float
              description: 航点 x 方向
            ori_y:
              type: float
              description: 航点 y 方向
            ori_z:
              type: float
              description: 航点 z 方向
            ori_w:
              type: float
              description: 航点 w 方向
            table_height:
              type: float
              description: 航点桌面高度
    """
    data = request.get_json()
    waypoint = Waypoint(
        waypointname=data["waypointname"],
        pos_x=data["pos_x"],
        pos_y=data["pos_y"],
        pos_z=data["pos_z"],
        ori_x=data["ori_x"],
        ori_y=data["ori_y"],
        ori_z=data["ori_z"],
        ori_w=data["ori_w"],
        table_height=data["table_height"],
    )
    db.session.add(waypoint)
    db.session.commit()
    return json_response(
        id=waypoint.id,
        waypointname=waypoint.waypointname,
        pos_x=waypoint.pos_x,
        pos_y=waypoint.pos_y,
        pos_z=waypoint.pos_z,
        ori_x=waypoint.ori_x,
        ori_y=waypoint.ori_y,
        ori_z=waypoint.ori_z,
        ori_w=waypoint.ori_w,
        table_height=waypoint.table_height,
    )


@waypoint_bp.route("/waypoints/<int:waypoint_id>", methods=["PUT"])
def update_waypoint(waypoint_id):
    """
    更新航点
    请求成功时，返回状态码 200。响应体包含一个 JSON 对象，其中包含更新的航点详情。
    ---
    tags:
      - Waypoint
    parameters:
      - in: path
        name: waypoint_id
        type: integer
    parameters:
      - in: body
        name: body
        required: true
        schema:
          id: WaypointUpdate
          properties:
            waypointname:
              type: string
              description: 航点名称
            pos_x:
              type: float
              description: 航点 x 坐标
            pos_y:
              type: float
              description: 航点 y 坐标
            pos_z:
              type: float
              description: 航点 z 坐标
            ori_x:
              type: float
              description: 航点 x 方向
            ori_y:
              type: float
              description: 航点 y 方向
            ori_z:
              type: float
              description: 航点 z 方向
            ori_w:
              type: float
              description: 航点 w 方向
            table_height:
              type: float
              description: 航点桌面高度
    responses:
      200:
        description: 更新航点成功
        schema:
          id: WaypointDetail
          properties:
            id:
              type: integer
              description: 航点 ID
            waypointname:
              type: string
              description: 航点名称
            pos_x:
              type: float
              description: 航点 x 坐标
            pos_y:
              type: float
              description: 航点 y 坐标
            pos_z:
              type: float
              description: 航点 z 坐标
            ori_x:
              type: float
              description: 航点 x 方向
            ori_y:
              type: float
              description: 航点 y 方向
            ori_z:
              type: float
              description: 航点 z 方向
            ori_w:
              type: float
              description: 航点 w 方向
            table_height:
                type: float
                description: 航点桌面高度
    """
    waypoint = Waypoint.query.get(waypoint_id)
    if waypoint is None:
        raise JsonError(description="Waypoint not found.")
    data = request.get_json()
    waypoint.waypointname = data["waypointname"]
    waypoint.pos_x = data["pos_x"]
    waypoint.pos_y = data["pos_y"]
    waypoint.pos_z = data["pos_z"]
    waypoint.ori_x = data["ori_x"]
    waypoint.ori_y = data["ori_y"]
    waypoint.ori_z = data["ori_z"]
    waypoint.ori_w = data["ori_w"]
    waypoint.table_height = data["table_height"]
    db.session.commit()
    return json_response(
        id=waypoint.id,
        waypointname=waypoint.waypointname,
        pos_x=waypoint.pos_x,
        pos_y=waypoint.pos_y,
        pos_z=waypoint.pos_z,
        ori_x=waypoint.ori_x,
        ori_y=waypoint.ori_y,
        ori_z=waypoint.ori_z,
        ori_w=waypoint.ori_w,
        table_height=waypoint.table_height,
    )


@waypoint_bp.route("/waypoints/<int:waypoint_id>", methods=["DELETE"])
def delete_waypoint(waypoint_id):
    """
    删除航点
    请求成功时，返回状态码 200。响应体为空。
    ---
    tags:
      - Waypoint
    parameters:
      - in: path
        name: waypoint_id
        type: integer
    responses:
      200:
        description: 删除航点成功
    """
    waypoint = Waypoint.query.get(waypoint_id)
    if waypoint is None:
        raise JsonError(description="Waypoint not found.")
    db.session.delete(waypoint)
    db.session.commit()
    return json_response()
