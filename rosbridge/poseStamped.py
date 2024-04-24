class PoseStamped:
    def __init__(self, frame_id, position_x, position_y, orientation_z, orientation_w):
        self.frame_id = frame_id
        self.position_x = position_x
        self.position_y = position_y
        self.position_z = 0
        self.orientation_x = 0
        self.orientation_y = 0
        self.orientation_z = orientation_z
        self.orientation_w = orientation_w

    def todict(self):
        return {
            "header": {
                "frame_id": self.frame_id
             },
            "pose": {
                "position": {
                    "x": self.position_x,
                    "y": self.position_y,
                    "z": self.position_z
                },
                "orientation": {
                    "x": self.orientation_x,
                    "y": self.orientation_y,
                    "z": self.orientation_z,
                    "w": self.orientation_w
                }
            }
        }

