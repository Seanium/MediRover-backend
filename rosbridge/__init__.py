import roslibpy

client = roslibpy.Ros(host='192.168.126.136', port=9090)
client.run()

print("ros_bridge connection is ", client.is_connected)
