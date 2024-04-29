from flask import Blueprint
from models.rx_model import Rx
from flask_json import JsonError, json_response, request
from database import db

rx_bp = Blueprint("rx_views", __name__)


@rx_bp.route("/rxs", methods=["GET"])
def get_rxs():
    """
    获取所有处方信息
    请求成功时，返回状态码 200。响应体包含一个 JSON 对象，其中包含处方信息列表。
    ---
    tags:
      - Rx
    responses:
      200:
        description: 获取处方信息成功
        schema:
          id: RxResponse
          properties:
            rxs:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    description: 处方 ID
                  name:
                    type: string
                    description: 处方名称
    """
    rxs = Rx.query.all()
    return json_response(
        rxs=[
            {
                "id": rx.id,
                "name": rx.name,
            }
            for rx in rxs
        ]
    )


@rx_bp.route("/rxs/<int:rx_id>", methods=["GET"])
def get_rx(rx_id):
    """
    获取指定处方的信息
    请求成功时，返回状态码 200。响应体包含一个 JSON 对象，其中包含指定处方的信息。
    ---
    tags:
      - Rx
    parameters:
      - name: rx_id
        in: path
        type: integer
        required: true
        description: 处方 ID
    responses:
      200:
        description: 获取处方信息成功
        schema:
          id: Rx
          properties:
            id:
              type: integer
              description: 处方 ID
            name:
              type: string
              description: 处方名称
    """
    rx = Rx.query.get(rx_id)
    if rx is None:
        raise JsonError(description="Not Found")
    return json_response(
        id=rx.id,
        name=rx.name,
    )


@rx_bp.route("/rxs", methods=["POST"])
def create_rx():
    """
    创建处方
    请求成功时，返回状态码 201。响应体包含一个 JSON 对象，其中包含新创建的处方信息。
    ---
    tags:
      - Rx
    parameters:
      - name: body
        in: body
        required: true
        schema:
          required:
            - name
          id: Rx
          properties:
            name:
              type: string
              description: 处方名称
    responses:
      201:
        description: 创建处方成功
        schema:
          id: Rx
          properties:
            id:
              type: integer
              description: 处方 ID
            name:
              type: string
              description: 处方名称
    """
    data = request.get_json()
    name = data.get("name")
    if name is None:
        raise JsonError(description="Bad Request")
    rx = Rx(name=name)
    db.session.add(rx)
    db.session.commit()
    return json_response(
        id=rx.id,
        name=rx.name,
    )


@rx_bp.route("/rxs/<int:rx_id>", methods=["PUT"])
def update_rx(rx_id):
    """
    更新处方
    请求成功时，返回状态码 200。响应体包含一个 JSON 对象，其中包含更新后的处方信息。
    ---
    tags:
      - Rx
    parameters:
      - name: rx_id
        in: path
        type: integer
        required: true
        description: 处方 ID
      - name: body
        in: body
        required: true
        schema:
          id: Rx
          properties:
            name:
              type: string
              description: 处方名称
    responses:
      200:
        description: 更新处方成功
        schema:
          id: Rx
          properties:
            id:
              type: integer
              description: 处方 ID
            name:
              type: string
              description: 处方名称
    """
    rx = Rx.query.get(rx_id)
    if rx is None:
        raise JsonError(description="Not Found")
    data = request.get_json()
    name = data.get("name")
    if name is None:
        raise JsonError(description="Bad Request")
    rx.name = name
    db.session.commit()
    return json_response(
        id=rx.id,
        name=rx.name,
    )


@rx_bp.route("/rxs/<int:rx_id>", methods=["DELETE"])
def delete_rx(rx_id):
    """
    删除处方
    请求成功时，返回状态码 204。
    ---
    tags:
      - Rx
    parameters:
      - name: rx_id
        in: path
        type: integer
        required: true
        description: 处方 ID
    responses:
      204:
        description: 删除处方成功
    """
    rx = Rx.query.get(rx_id)
    if rx is None:
        raise JsonError(description="Not Found")
    db.session.delete(rx)
    db.session.commit()
    return "", 204
