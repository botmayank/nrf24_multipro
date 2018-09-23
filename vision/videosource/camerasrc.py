import time

import cv2
import numpy as np


class CameraSrc:
    _use_rtsp = True

    def __init__(self):
        self.camera = None
        if self._use_rtsp:
            self.camera = cv2.VideoCapture("rtsp://%s:%d/%s" % ("192.168.31.111", 8554, "play"))
        else:
            # self.camera = cv2.VideoCapture("../../media/syma_aruco_4x4_17_short_2.mp4")
            # self.camera = cv2.VideoCapture("../../media/single_marker.mp4")
            self.camera = cv2.VideoCapture("../../media/single_height.mp4")

        self.camera_matrix = np.array([[989.43041893, 0., 643.65628421],
                                       [0., 992.17579024, 342.38060762],
                                       [0., 0., 1.]])
        self.dist_matrix = np.array([2.13212094e-01, -1.78417926e+00, -2.79719436e-03, -2.82407212e-03, 8.10910900e+00])

    def __del__(self):
        if self.camera is not None:
            self.camera.release()

    def grab_frame(self):
        ret, frame = self.camera.read()
        return frame if ret else None


if __name__ == '__main__':
    cam = CameraSrc()
    while True:
        frame = cam.grab_frame()
        cv2.waitKey(1)
        cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('frame', 640, 360)
        cv2.imshow('frame', frame)
        k = cv2.waitKey(1)
        if k == ord('q'):
            break
        elif k == ord('w'):
            time.sleep(3)
    del cam
