from flask import Blueprint
from models.robot_model import Robot
from flask_json import JsonError, json_response, request
from database import db

robot_bp = Blueprint("robot_views", __name__)


@robot_bp.route("/robots", methods=["GET"])
@robot_bp.route("/robots", methods=["GET"])
def get_robots():
    """
    获取所有机器人信息
    请求成功时，返回状态码 200。响应体包含一个 JSON 对象，其中包含机器人信息列表。
    ---
    tags:
      - Robot
    responses:
      200:
        description: 获取机器人信息成功
        schema:
          id: RobotResponse
          properties:
            robots:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    description: 机器人 ID
                  robot_status:
                    type: string
                    description: 机器人状态
                  robot_ip:
                    type: string
                    description: 机器人 IP
    """
    robots = Robot.query.all()
    return json_response(
        robots=[
            {
                "id": robot.id,
                "robot_status": robot.robot_status,
                "robot_ip": robot.robot_ip,
            }
            for robot in robots
        ]
    )


@robot_bp.route("/robots/<int:robot_id>", methods=["GET"])
def get_robot(robot_id):
    """
    获取指定机器人的信息
    请求成功时，返回状态码 200。响应体包含一个 JSON 对象，其中包含指定机器人的信息。
    ---
    tags:
      - Robot
    parameters:
      - in: path
        name: robot_id
        type: integer
        required: true
        description: 机器人 ID
    responses:
      200:
        description: 获取机器人信息成功
        schema:
          id: RobotDetail
          properties:
            id:
              type: integer
              description: 机器人 ID
            robot_status:
              type: string
              description: 机器人状态
            robot_ip:
              type: string
              description: 机器人 IP
    """
    robot = Robot.query.get(robot_id)
    if robot is None:
        raise JsonError(description="Robot not found.")
    return json_response(
        id=robot.id,
        robot_status=robot.robot_status,
        robot_ip=robot.robot_ip,
    )


@robot_bp.route("/robots", methods=["POST"])
def create_robot():
    """
    创建新的机器人信息
    请求成功时，返回状态码 200。响应体包含一个 JSON 对象，其中包含新创建的机器人信息。
    ---
    tags:
      - Robot
    parameters:
      - in: body
        name: body
        required: true
        schema:
          id: RobotCreate
          required:
            - robot_status
            - robot_ip
          properties:
            robot_status:
              type: string
              description: 机器人状态
            robot_ip:
              type: string
              description: 机器人 IP
    responses:
      200:
        description: 创建机器人信息成功
        schema:
          id: RobotDetail
          properties:
            id:
              type: integer
              description: 机器人 ID
            robot_status:
              type: string
              description: 机器人状态
            robot_ip:
              type: string
              description: 机器人 IP
    """
    data = request.get_json()
    robot = Robot(
        robot_status=data["robot_status"],
        robot_ip=data["robot_ip"],
    )
    db.session.add(robot)
    db.session.commit()
    return json_response(
        id=robot.id,
        robot_status=robot.robot_status,
        robot_ip=robot.robot_ip,
    )


@robot_bp.route("/robots/<int:robot_id>", methods=["PUT"])
def update_robot(robot_id):
    """
    更新指定机器人的信息
    请求成功时，返回状态码 200。响应体包含一个 JSON 对象，其中包含更新后的机器人信息。
    ---
    tags:
      - Robot
    parameters:
      - in: path
        name: robot_id
        type: integer
        required: true
        description: 机器人 ID
      - in: body
        name: body
        schema:
          id: RobotUpdate
          required:
            - robot_status
            - robot_ip
          properties:
            robot_status:
              type: string
              description: 机器人状态
            robot_ip:
              type: string
              description: 机器人 IP
    responses:
      200:
        description: 更新机器人信息成功
        schema:
          id: RobotDetail
          properties:
            id:
              type: integer
              description: 机器人 ID
            robot_status:
              type: string
              description: 机器人状态
            robot_ip:
              type: string
              description: 机器人 IP
    """
    robot = Robot.query.get(robot_id)
    if robot is None:
        raise JsonError(description="Robot not found.")

    data = request.get_json() or {}
    if "robot_status" in data and "robot_ip" in data:
        robot.robot_status = data["robot_status"]
        robot.robot_ip = data["robot_ip"]
    else:
        raise JsonError(description="Missing fields.")

    db.session.commit()
    return json_response(
        id=robot.id,
        robot_status=robot.robot_status,
        robot_ip=robot.robot_ip,
    )


@robot_bp.route("/robots/<int:robot_id>", methods=["DELETE"])
def delete_robot(robot_id):
    """
    删除指定的机器人
    请求成功时，返回状态码 200。响应体为空。
    ---
    tags:
      - Robot
    parameters:
      - in: path
        name: robot_id
        type: integer
        required: true
        description: 机器人 ID
    responses:
      200:
        description: 删除机器人成功
    """
    robot = Robot.query.get(robot_id)
    if robot is None:
        raise JsonError(description="Robot not found.")

    db.session.delete(robot)
    db.session.commit()

    return json_response()
