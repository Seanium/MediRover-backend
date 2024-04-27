import roslibpy
import time
from rosbridge.__init__ import client
from rosbridge.poseStamped import PoseStamped
from rosbridge.exception_table import ExceptionTable


def transport_cmd(start_pos: PoseStamped, target_pos: PoseStamped, origin_pos: PoseStamped, table_height):
    """
    向ROS端发送送药命令
    :param start_pos: 药房坐标
    :param target_pos: 病床坐标
    :param origin_pos: 待机点
    :param table_height: 病床床头柜高度
    :return:
    """
    send_goal_topic = roslibpy.Topic(client, "/transport_cmd", "medirover_pkg/transport_cmd")
    goal_msg = roslibpy.Message({
        "start_pos": start_pos.todict(),
        "target_pos": target_pos.todict(),
        "origin_pos": origin_pos.todict(),
        "table_height": {"data": table_height}
    })
    print('Sending transport message...')
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


def exception_cmd(exc_type: int):
    """
    向ROS发出异常处理指令，其中异常类型参见exception_table.py
    :return:
    """
    interrupt_topic = roslibpy.Topic(client, "/exception_cmd", "std_msgs/String")
    if exc_type == ExceptionTable.interrupt:
        exc_cmd = roslibpy.Message({"data": "interrupt"})
        print("sending interrupt message...")
    if exc_type == ExceptionTable.recover:
        exc_cmd = roslibpy.Message({"data": "recover"})
        print("sending recover message...")
    interrupt_topic.publish(exc_cmd)
    time.sleep(1)


def mapping_cmd(cmd: str):
    """
    向ROS发送建图命令
    :param cmd: 从以下模式中选择一个：start,save,end
    :return:
    """
    mapping_topic = roslibpy.Topic(client, "/bd_map_cmd", "std_msgs/String")
    mapping_topic.publish(roslibpy.Message({"data": cmd}))
    print("sending mapping message...")
    time.sleep(1)


def vel_ctrl_cmd(cmd: str):
    """
    向ROS发送移动控制命令
    :param cmd: 从以下模式中选择一个：stop,front,back,left,right,turn_left,turn_right
    :return:
    """
    vel_ctrl_topic = roslibpy.Topic(client, "/cli_vel_ctrl", "std_msgs/String")
    vel_ctrl_topic.publish(roslibpy.Message({"data": cmd}))
    print("sending vel_ctrl message...")
    time.sleep(1)


if __name__ == '__main__':
    def app_transport():
        start_pos = PoseStamped("map", 0.12, 1.73, 0, 1)
        target_pos = PoseStamped("map", -4.36, -1.60, 0, 1)
        origin_pos = PoseStamped("map", 0, 0, 0, 1)
        table_height = 0.7
        transport_cmd(start_pos, target_pos, origin_pos, table_height)


    def app_cruise():
        pos1 = PoseStamped("map", -4.09, 1.31, 0.70, 0.71)
        pos2 = PoseStamped("map", -1.46, -1.63, -0.70, 0.70)
        pos3 = PoseStamped("map", 4.05, -1.78, -0.70, 0.70)
        origin_pos = PoseStamped("map", 0, 0, 0, 1)
        poses = [pos1, pos2, pos3, origin_pos]
        cruise_cmd(poses)

    # 调用方式：
    # app_transport()
    # exception_cmd(ExceptionTable.interrupt)
    # exception_cmd(ExceptionTable.recover)
    # app_cruise()
    # mapping_cmd("start")
    # mapping_cmd("save")
    # mapping_cmd("end")
    # vel_ctrl_cmd("stop")
    # vel_ctrl_cmd("front")
    # vel_ctrl_cmd("back")
    # vel_ctrl_cmd("left")
    # vel_ctrl_cmd("right")
    # vel_ctrl_cmd("turn_left")
    # vel_ctrl_cmd("turn_right")
