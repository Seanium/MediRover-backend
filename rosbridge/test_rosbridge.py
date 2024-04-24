import roslibpy
import time
from rosbridge.__init__ import client
from rosbridge.poseStamped import PoseStamped


def transport_cmd(start_pos: PoseStamped, target_pos: PoseStamped, origin_pos: PoseStamped, table_height):
    """
    向ROS端发送送药命令
    :param start_pos: 药房坐标
    :param target_pos: 病床坐标
    :param origin_pos: 待机点
    :param table_height: 病床床头柜高度
    :return:
    """
    send_goal_topic = roslibpy.Topic(client, "/transport_commend", "medirover_pkg/transport_cmd")
    goal_msg = roslibpy.Message({
        "start_pos": start_pos.todict(),
        "target_pos": target_pos.todict(),
        "origin_pos": origin_pos.todict(),
        "table_height": {"data": table_height}
    })
    print('Sending message...')
    send_goal_topic.publish(goal_msg)
    time.sleep(1)


def cruise_cmd(target_poses: list = None):
    """
    Send position of cruise targets to robot.
    The last element of "poses" must be the original point where robot will return after accomplishing cruise mission.
    :param target_poses:
    :return:
    """
    send_goal_topic = roslibpy.Topic(client, "/cruise_cmd", "geometry_msgs/PoseArray")
    poses = [(i.todict())["pose"] for i in target_poses]
    poses.reverse()
    goal_msg = roslibpy.Message({
        "header": {
            "frame_id": "map"
        },
        "poses": poses
    })
    print('Sending cruise message...')
    send_goal_topic.publish(goal_msg)
    time.sleep(1)
