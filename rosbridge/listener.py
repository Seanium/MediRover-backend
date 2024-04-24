import roslibpy

from rosbridge.__init__ import client


def transport_listen(message: dict):
    """
    监听'/transport_status'话题发来的消息
    :param message: 格式{‘data’: (string)xxx}
    :return:
    """
    # print('get transport status: ' + message['data'])


def cruise_listen(message: dict):
    """
    监听'/transport_status'话题发来的消息
    :param message: 格式{‘data’: (string)xxx}
    :return:
    """
    print('get cruise status: ' + message['data'])


if __name__ == '__main__':
    transport_listener = roslibpy.Topic(client, '/transport_status', 'std_msgs/String')
    transport_listener.subscribe(transport_listen)
    cruise_listener = roslibpy.Topic(client, '/cruise_status', 'std_msgs/String')
    cruise_listener.subscribe(cruise_listen)
    try:
        while True:
            pass
    except KeyboardInterrupt:
        client.terminate()
