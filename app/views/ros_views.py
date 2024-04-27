from flask import Blueprint
from json_response import JsonResponse

# from rosbridge.test_rosbridge import transport_cmd, cruise_cmd
# from rosbridge.poseStamped import PoseStamped

ros_bp = Blueprint("ros_views", __name__)


@ros_bp.route("/transport", methods=["POST"])
def ros_bp_transport():
    start_pos = PoseStamped("map", 0.12, 1.73, 0, 1)
    target_pos = PoseStamped("map", -4.36, -1.60, 0, 1)
    origin_pos = PoseStamped("map", 0, 0, 0, 1)
    table_height = 0.7
    transport_cmd(start_pos, target_pos, origin_pos, table_height)
    return JsonResponse.success()


@ros_bp.route("/cruise", methods=["POST"])
def ros_bp_cruise():
    pos1 = PoseStamped("map", -4.09, 1.31, 0.70, 0.71)
    pos2 = PoseStamped("map", -1.46, -1.63, -0.70, 0.70)
    pos3 = PoseStamped("map", 4.05, -1.78, -0.70, 0.70)
    origin_pos = PoseStamped("map", 0, 0, 0, 1)
    poses = [pos1, pos2, pos3, origin_pos]
    cruise_cmd(poses)
    return JsonResponse.success()
