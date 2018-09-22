class Pose:
    def __init__(self):
        # distance from the camera
        self.z = 0
        # pose from estimateArucoPose - actual distance of camera from marker incorporating height
        self.dist_x = 0
        self.dist_y = 0
        # pixel position x,y
        self.px = 0
        self.py = 0
        self.yaw = 0
