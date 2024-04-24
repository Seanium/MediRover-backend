from flask_cors import CORS
from flask import request
import json
import sys
import os

from json_flask import JsonFlask
from json_response import JsonResponse
from rosbridge.test_rosbridge import transport_cmd, cruise_cmd
from rosbridge.poseStamped import PoseStamped

# 创建视图应用
app = JsonFlask(__name__)
# 解决跨域
CORS(app, supports_credentials=True)
# 处理本地文件路径
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)


# 类型转换或返回默认值
def get_req_value(key: str, target_type: str, from_data: bool = True):
    if from_data:
        data = json.loads(request.data)
        if target_type == "int":
            if data.get(key, None) is not None and data[key] != "":
                return int(data[key])
            else:
                return 0
        if target_type == "float":
            if data.get(key, None) is not None and data[key] != "":
                return float(data[key])
            else:
                return 0.0
        if target_type == "str":
            if data.get(key, None) is not None and data[key] != "" and data[key] != "\"\"" and data[key] != "\'\'":
                return data[key]
            else:
                return ""
        if target_type == "order":
            if data.get(key, None) is not None and data[key] != "":
                return tuple(data[key].split(','))
            else:
                return ()
    else:
        if target_type == "int":
            if request.args.get(key) is not None and request.args.get(key) != "":
                return int(request.args.get(key))
            else:
                return 0
        if target_type == "float":
            if request.args.get(key) is not None and request.args.get(key) != "":
                return float(request.args.get(key))
            else:
                return 0.0
        if target_type == "str":
            if request.args.get(key) is not None and request.args.get(key) != "" and request.args.get(
                    key) != "\"\"" and request.args.get(key) != "\'\'":
                return request.args.get(key)
            else:
                return ""
        if target_type == "order":
            if request.args.get(key) is not None and request.args.get(key) != "":
                return tuple(request.args.get(key).split(','))
            else:
                return ()


@app.route("/transport", methods=["POST"])
def app_transport():
    start_pos = PoseStamped("map", 0.12, 1.73, 0, 1)
    target_pos = PoseStamped("map", -4.36, -1.60, 0, 1)
    origin_pos = PoseStamped("map", 0, 0, 0, 1)
    table_height = 0.7
    transport_cmd(start_pos, target_pos, origin_pos, table_height)
    return JsonResponse.success()


@app.route("/cruise", methods=["POST"])
def app_cruise():
    pos1 = PoseStamped("map", -4.09, 1.31, 0.70, 0.71)
    pos2 = PoseStamped("map", -1.46, -1.63, -0.70, 0.70)
    pos3 = PoseStamped("map", 4.05, -1.78, -0.70, 0.70)
    origin_pos = PoseStamped("map", 0, 0, 0, 1)
    poses = [pos1, pos2, pos3, origin_pos]
    cruise_cmd(poses)
    return JsonResponse.success()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
