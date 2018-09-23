import time


def precision(val):
    return round(val, 2)


current_millis = lambda: int(round(time.time() * 1000))


class Pose:
    UNKNOWN = 190220

    def __init__(self, px, py, marker_length, dist_x=UNKNOWN, dist_y=UNKNOWN, dist_z=UNKNOWN, yaw=UNKNOWN):
        # pose from estimateArucoPose - actual distance of camera from marker incorporating height
        self.dist_x = precision(dist_x)
        self.dist_y = precision(dist_y)
        # distance from the camera
        self.dist_z = precision(dist_z)
        # pixel position x,y
        self.px = precision(px)
        self.py = precision(py)
        self.marker_length = precision(marker_length)
        self.yaw = precision(yaw)
        self.time = current_millis
