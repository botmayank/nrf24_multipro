from vision.aruco.aruco_finder import ArucoFinder
from vision.aruco.pose import Pose

syma = None
aruco_finder = None

PORT = "/dev/ttyUSB0"


def get_pose():
    return aruco_finder.run_camera_and_detect(True, syma.values())


def control():
    delta = 0.3
    while True:
        pose = get_pose()
        if pose is not None:
            syma.pitch(delta if pose.px > 20 else -delta if pose.px < -20 else 0)
            syma.roll(delta if pose.py > 20 else -delta if pose.py < -20 else 0)

            if pose.yaw != Pose.UNKNOWN:
                if 100 < pose.yaw <= 270:
                    syma.yaw(-delta)
                elif 80 > pose.yaw >= 0 or 270 < pose.yaw <= 360:
                    syma.yaw(delta)
                else:
                    syma.yaw(0)

            if pose.dist_z == Pose.UNKNOWN:
                syma.throttle = 1530
            elif pose.dist_z >= 150:
                syma.delta_thrust_relative(delta)
            elif pose.dist_z <= 130:
                syma.delta_thrust_relative(-delta)
            else:
                syma.level_throttle()
        else:
            syma.reset_rotation()
            syma.level_throttle()

        print(syma.values())
        syma.send_command()


if __name__ == '__main__':
    try:
        aruco_finder = ArucoFinder()

        control()
    except KeyboardInterrupt:
        pass
    finally:
        # Cleanly exit
        del syma
        del aruco_finder
