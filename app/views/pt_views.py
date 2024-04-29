from flask import Blueprint
from models.pt_model import Pt
from flask_json import JsonError, json_response, request
from database import db

pt_bp = Blueprint("pt_views", __name__)


@pt_bp.route("/pts", methods=["GET"])
def get_pts():
    """
    获取所有患者信息
    请求成功时，返回状态码 200。响应体包含一个 JSON 对象，其中包含患者信息列表。
    ---
    tags:
      - Pt
    responses:
      200:
        description: 获取患者信息成功
        schema:
          id: PtResponse
          properties:
            pts:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    description: 患者 ID
                  name:
                    type: string
                    description: 患者名称
                  waypoint_id:
                    type: integer
                    description: 病床航点 ID
    """
    pts = Pt.query.all()
    return json_response(
        pts=[
            {
                "id": pt.id,
                "name": pt.name,
                "waypoint_id": pt.waypoint_id,
            }
            for pt in pts
        ]
    )


@pt_bp.route("/pts/<int:pt_id>", methods=["GET"])
def get_pt(pt_id):
    """
    获取指定患者的信息
    请求成功时，返回状态码 200。响应体包含一个 JSON 对象，其中包含指定患者的信息。
    ---
    tags:
      - Pt
    parameters:
      - name: pt_id
        in: path
        type: integer
        required: true
        description: 患者 ID
    responses:
      200:
        description: 获取患者信息成功
        schema:
          id: PtResponse
          properties:
            id:
              type: integer
              description: 患者 ID
            name:
              type: string
              description: 患者名称
            waypoint_id:
              type: integer
              description: 病床航点 ID
    """
    pt = Pt.query.get(pt_id)
    if pt is None:
        raise JsonError(description="Not Found")
    return json_response(
        id=pt.id,
        name=pt.name,
        waypoint_id=pt.waypoint_id,
    )


@pt_bp.route("/pts", methods=["POST"])
def create_pt():
    """
    创建患者
    请求成功时，返回状态码 201。响应体包含一个 JSON 对象，其中包含新患者的信息。
    ---
    tags:
      - Pt
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Pt
          properties:
            name:
              type: string
              description: 患者名称
            waypoint_id:
              type: integer
              description: 病床航点 ID
    responses:
      201:
        description: 创建患者成功
        schema:
          id: PtResponse
          properties:
            id:
              type: integer
              description: 患者 ID
            name:
              type: string
              description: 患者名称
            waypoint_id:
              type: integer
              description: 病床航点 ID
    """
    data = request.get_json()
    pt = Pt(name=data["name"], waypoint_id=data["waypoint_id"])
    db.session.add(pt)
    db.session.commit()
    return json_response(
        id=pt.id,
        name=pt.name,
        waypoint_id=pt.waypoint_id,
    )


@pt_bp.route("/pts/<int:pt_id>", methods=["PUT"])
def update_pt(pt_id):
    """
    更新患者信息
    请求成功时，返回状态码 200。响应体为空。
    ---
    tags:
      - Pt
    parameters:
      - name: pt_id
        in: path
        type: integer
        required: true
        description: 患者 ID
      - name: body
        in: body
        required: true
        schema:
          id: Pt
          properties:
            name:
              type: string
              description: 患者名称
            waypoint_id:
              type: integer
              description: 病床航点 ID
    responses:
      200:
        description: 更新患者信息成功
    """
    pt = Pt.query.get(pt_id)
    if pt is None:
        raise JsonError(description="Not Found")
    data = request.get_json()
    pt.name = data["name"]
    pt.waypoint_id = data["waypoint_id"]
    db.session.commit()
    return json_response()


@pt_bp.route("/pts/<int:pt_id>", methods=["DELETE"])
def delete_pt(pt_id):
    """
    删除患者
    请求成功时，返回状态码 204。响应体为空。
    ---
    tags:
      - Pt
    parameters:
      - name: pt_id
        in: path
        type: integer
        required: true
        description: 患者 ID
    responses:
      204:
        description: 删除患者成功
    """
    pt = Pt.query.get(pt_id)
    if pt is None:
        raise JsonError(description="Not Found")
    db.session.delete(pt)
    db.session.commit()
    return json_response()
