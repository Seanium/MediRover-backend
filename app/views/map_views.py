from flask import Blueprint
from models.map_model import Map
from flask_json import JsonError, json_response, request
from database import db

map_bp = Blueprint("map_views", __name__)


@map_bp.route("/maps", methods=["GET"])
def maps():
    """
    获取地图列表
    请求成功时，返回状态码 200。响应体包含一个 JSON 对象，其中包含地图列表。
    ---
    tags:
      - Map
    responses:
      200:
        description: 获取地图列表成功
        schema:
          id: MapResponse
          properties:
            maps:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    description: 地图 ID
                  mapname:
                    type: string
                    description: 地图名称
                  mappath:
                    type: string
                    description: 地图路径
                  waypointpath:
                    type: string
                    description: 航点文件路径
    """
    maps = Map.query.all()
    return json_response(
        maps=[
            {
                "id": map.id,
                "mapname": map.mapname,
                "mappath": map.mappath,
                "waypointpath": map.waypointpath,
            }
            for map in maps
        ]
    )


@map_bp.route("/maps/<int:map_id>", methods=["GET"])
def map_detail(map_id):
    """
    获取地图详情
    请求成功时，返回状态码 200。响应体包含一个 JSON 对象，其中包含地图详情。
    ---
    tags:
      - Map
    parameters:
      - in: path
        name: map_id
        type: integer
        required: true
        description: 地图 ID
    responses:
      200:
        description: 获取地图详情成功
        schema:
          id: MapDetailResponse
          properties:
            id:
              type: integer
              description: 地图 ID
            mapname:
              type: string
              description: 地图名称
            mappath:
              type: string
              description: 地图路径
            waypointpath:
              type: string
              description: 航点文件路径
      404:
        description: 地图不存在
    """
    map = Map.query.get(map_id)
    if map is None:
        raise JsonError(description="地图不存在")
    return json_response(
        id=map.id,
        mapname=map.mapname,
        mappath=map.mappath,
        waypointpath=map.waypointpath,
    )


@map_bp.route("/maps", methods=["POST"])
def create_map():
    """
    创建地图
    请求成功时，返回状态码 200。响应体包含一个 JSON 对象，其中包含创建的地图信息。
    ---
    tags:
      - Map
    parameters:
      - in: body
        name: body
        schema:
          id: CreateMapRequest
          required:
            - mapname
            - mappath
            - waypointpath
          properties:
            mapname:
              type: string
              description: 地图名称
            mappath:
              type: string
              description: 地图路径
            waypointpath:
              type: string
              description: 航点文件路径
    responses:
      200:
        description: 地图创建成功
        schema:
          id: MapResponse
          properties:
            id:
              type: integer
              description: 地图 ID
            mapname:
              type: string
              description: 地图名称
            mappath:
              type: string
              description: 地图路径
            waypointpath:
              type: string
              description: 航点文件路径
      400:
        description: 请求错误，可能的原因包括地图名称、地图路径和航点文件路径不能为空，或地图名称已存在
    """
    mapname = request.json.get("mapname")
    mappath = request.json.get("mappath")
    waypointpath = request.json.get("waypointpath")
    if mapname is None or mappath is None or waypointpath is None:
        raise JsonError(description="地图名称、地图路径和航点文件路径不能为空")
    if Map.query.filter_by(mapname=mapname).first() is not None:
        raise JsonError(description=f"地图名称为 {mapname} 的地图已存在")
    map = Map(mapname=mapname, mappath=mappath, waypointpath=waypointpath)
    db.session.add(map)
    db.session.commit()
    return json_response(
        id=map.id,
        mapname=map.mapname,
        mappath=map.mappath,
        waypointpath=map.waypointpath,
    )


@map_bp.route("/maps/<int:map_id>", methods=["PUT"])
def update_map(map_id):
    """
    更新地图
    请求成功时，返回状态码 200。响应体包含一个 JSON 对象，其中包含更新的地图信息。
    ---
    tags:
      - Map
    parameters:
      - in: path
        name: map_id
        type: integer
        required: true
        description: 地图 ID
      - in: body
        name: body
        schema:
          id: UpdateMapRequest
          required:
            - mapname
            - mappath
            - waypointpath
          properties:
            mapname:
              type: string
              description: 地图名称
            mappath:
              type: string
              description: 地图路径
            waypointpath:
              type: string
              description: 航点文件路径
    responses:
      200:
        description: 地图更新成功
        schema:
          id: MapResponse
          properties:
            id:
              type: integer
              description: 地图 ID
            mapname:
              type: string
              description: 地图名称
            mappath:
              type: string
              description: 地图路径
            waypointpath:
              type: string
              description: 航点文件路径
      404:
        description: 地图不存在
      400:
        description: 请求错误，可能的原因包括地图名称、地图路径和航点文件路径不能为空，或地图名称已存在
    """
    map = Map.query.get(map_id)
    if map is None:
        raise JsonError(description="地图不存在")
    mapname = request.json.get("mapname")
    mappath = request.json.get("mappath")
    waypointpath = request.json.get("waypointpath")
    if mapname is None or mappath is None or waypointpath is None:
        raise JsonError(description="地图名称、地图路径和航点文件路径不能为空")
    if Map.query.filter_by(mapname=mapname).first() is not None:
        raise JsonError(description=f"地图名称为 {mapname} 的地图已存在")
    map.mapname = mapname
    map.mappath = mappath
    map.waypointpath = waypointpath
    db.session.commit()
    return json_response(
        id=map.id,
        mapname=map.mapname,
        mappath=map.mappath,
        waypointpath=map.waypointpath,
    )


@map_bp.route("/maps/<int:map_id>", methods=["DELETE"])
def delete_map(map_id):
    """
    删除地图
    请求成功时，返回状态码 200。响应体包含一个 JSON 对象，其中包含删除的地图信息。
    ---
    tags:
      - Map
    parameters:
      - in: path
        name: map_id
        type: integer
        required: true
        description: 地图 ID
    responses:
      200:
        description: 地图删除成功
        schema:
          id: MapResponse
          properties:
            id:
              type: integer
              description: 地图 ID
            mapname:
              type: string
              description: 地图名称
            mappath:
              type: string
              description: 地图路径
            waypointpath:
              type: string
              description: 航点文件路径
      404:
        description: 地图不存在
    """
    map = Map.query.get(map_id)
    if map is None:
        raise JsonError(description="地图不存在")
    db.session.delete(map)
    db.session.commit()
    return json_response(
        id=map.id,
        mapname=map.mapname,
        mappath=map.mappath,
        waypointpath=map.waypointpath,
    )
