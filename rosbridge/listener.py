import roslibpy

client = roslibpy.Ros(host="192.168.5.131", port=9090)
client.run()

print("ros_bridge connection is ", client.is_connected)


def transport_listen(message: dict):
    """
    监听'/transport_status'话题发来的消息，该话题中发布的是 送药业务的执行状态
    :param message: 格式{‘data’: (string)xxx}
    :return:
    """
    print("get transport status: " + message["data"])


def cruise_listen(message: dict):
    """
    监听'/transport_status'话题发来的消息，该话题中发布的是 巡诊业务的执行状态
    :param message: 格式{‘data’: (string)xxx}
    :return:
    """
    print("get cruise status: " + message["data"])


def tp_req_listen(message: dict):
    """
    监听'/take_tp_req'话题发来的消息，该话题中发布的是 测温请求
    :param message: 格式{‘data’: (string)xxx}
    :return:
    """
    print("get take temperature request: " + message["data"])


def tp_result_listen(message: dict):
    """
    监听'/tp_result'话题发来的消息，该话题中发布的是 测温结果
    :param message: 格式{‘data’: (float)xxx}，其中xxx是float类型的
    :return:
    """
    print("get body temperature: " + message["data"])


if __name__ == "__main__":
    transport_listener = roslibpy.Topic(client, "/transport_status", "std_msgs/String")
    transport_listener.subscribe(transport_listen)
    cruise_listener = roslibpy.Topic(client, "/cruise_status", "std_msgs/String")
    cruise_listener.subscribe(cruise_listen)
    tp_req_listener = roslibpy.Topic(client, "/take_tp_req", "std_msgs/String")
    tp_req_listener.subscribe(tp_req_listen)
    tp_result_listener = roslibpy.Topic(client, "/tp_result", "std_msgs/Float32")
    tp_result_listener.subscribe(tp_result_listen)
    try:
        while True:
            pass
    except KeyboardInterrupt:
        client.terminate()
